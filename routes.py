from bson import ObjectId
from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Query
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from models import Movie, MovieUpdate  # Ajustez les importations en fonction de vos modèles

router = APIRouter()

# Fonction pour convertir les ObjectId de MongoDB en chaîne de caractères
def convert_objectid_to_str(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, dict):
        return {key: convert_objectid_to_str(value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [convert_objectid_to_str(item) for item in obj]
    return obj

# Route pour lister tous les films
@router.get("/", response_description="Liste de tous les films", response_model=List[Movie])
def list_movies(request: Request):
    # Récupérer les films de la base de données MongoDB
    movies = list(request.app.database["movies"].find(limit=100))
    # Convertir les ObjectId en chaînes de caractères
    movies = convert_objectid_to_str(movies)
    return movies

# Route pour rechercher des films par titre ou acteur
@router.get("/search", response_description="Rechercher un film par titre ou acteur", response_model=List[Movie])
async def search_movies(
        request: Request,
        title: Optional[str] = Query(None, title="Titre"),
        actor: Optional[str] = Query(None, title="Acteur ")
):
    query = {}

    # Si un titre est spécifié, ajouter un filtre de recherche par titre (insensible à la casse)
    if title:
        query["title"] = {"$regex": title, "$options": "i"}

    # Si un acteur est spécifié, ajouter un filtre de recherche par acteur (insensible à la casse)
    if actor:
        query["cast"] = {"$regex": actor, "$options": "i"}

    # Récupérer les films qui correspondent aux critères de recherche
    movies = request.app.database["movies"].find(query)
    movies_list = convert_objectid_to_str(list(movies))

    # Si aucun film n'est trouvé, lancer une exception HTTP 404
    if not movies_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun film trouvé avec ces critères")
    
    return movies_list

# Route pour mettre à jour un film en fonction de son titre
@router.put("/{title}", response_description="Mettre à jour un film par son titre", response_model=Movie)
def update_movie(title: str, request: Request, movie: MovieUpdate = Body(...)):
    # Créer un dictionnaire des champs à mettre à jour (ignorer ceux qui sont à None)
    movie_dict = {k: v for k, v in movie.dict().items() if v is not None}

    # Si aucun champ valide n'est fourni, lancer une exception HTTP 400
    if not movie_dict:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Aucun champ valide fourni pour la mise à jour")

    # Mettre à jour le film dans la base de données MongoDB
    update_result = request.app.database["movies"].update_one(
        {"title": title}, {"$set": movie_dict}
    )

    # Si aucune modification n'a été effectuée (film non trouvé), lancer une exception HTTP 404
    if update_result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Film avec le titre '{title}' non trouvé")

    # Récupérer le film mis à jour
    updated_movie = convert_objectid_to_str(request.app.database["movies"].find_one({"title": title}))

    return updated_movie

# Route pour récupérer les films communs entre MongoDB et Neo4j
@router.get("/common-movies", response_description="Récupérer les films communs entre MongoDB et Neo4j")
def get_common_movies(request: Request):
    # Récupérer les titres des films depuis MongoDB
    mongodb_titles = set(movie["title"] for movie in request.app.database["movies"].find({}, {"title": 1}))
    
    # Récupérer les titres des films depuis Neo4j
    with request.app.neo4j_driver.session() as session:
        neo4j_titles = set(record["title"] for record in session.run("MATCH (m:Movie) RETURN m.title AS title"))

    # Trouver l'intersection des titres de films entre MongoDB et Neo4j
    common_titles = list(mongodb_titles & neo4j_titles)

    return {"common_movies_count": len(common_titles), "common_movies": common_titles}

# Route pour lister les utilisateurs ayant évalué un film donné
@router.get("/movies/{title}/users", response_description="Lister les utilisateurs ayant évalué un film")
def list_users_who_rated_movie(title: str, request: Request):
    # Exécuter une requête dans Neo4j pour récupérer les utilisateurs ayant évalué le film
    with request.app.neo4j_driver.session() as session:
        query = """
        MATCH (p:Person)-[rel:REVIEWED]->(m:Movie)
        WHERE toLower(m.title) CONTAINS toLower($title)
        RETURN m.title AS movie_title, collect(p.name) AS users
        """
        result = session.run(query, title=title)
        
        # Si aucun film n'est trouvé, retourner une erreur 404
        if not result:
            raise HTTPException(status_code=404, detail="Aucun film trouvé avec ce terme de recherche.")
        
        # Préparer la réponse structurée avec les films et les utilisateurs associés
        response = []
        for record in result:
            response.append({
                "movie title": record["movie_title"],
                "users": record["users"]
            })
        
        return {"search title": title, "movies": response}

# Route pour lister les films évalués par un utilisateur donné
@router.get("/users/{name}/rated-movies")
def get_user_rated_movies(name: str, request: Request):
    # Exécuter une requête dans Neo4j pour récupérer les films évalués par l'utilisateur
    with request.app.neo4j_driver.session() as session:
        query = """
        MATCH (p:Person)-[rel:REVIEWED]->(m:Movie)
        WHERE toLower(p.name) CONTAINS toLower($name)
        RETURN p.name AS user_name, count(rel) AS rated_count, collect(m.title) AS movies
        """
        result = session.run(query, name=name)
        
        users = []
        for record in result:
            users.append({
                "user": record["user_name"],
                "number of rated films": record["rated_count"],
                "movies": record["movies"]
            })

        # Si aucun utilisateur n'est trouvé, retourner une erreur 404
        if not users:
            raise HTTPException(status_code=404, detail="Aucun utilisateur trouvé avec ce nom.")
        
        return {"user found": users}
