# API de Gestion des Films - Final Lab

Ce projet est une application Python permettant de gérer et d'analyser des données sur les films et les utilisateurs en utilisant les bases de données **MongoDB** et **Neo4j**. L'API REST, implémentée avec **FastAPI**, permet de réaliser des opérations CRUD ainsi que des analyses croisées sur les données.

---

## Table des Matières

1. [Introduction](#introduction)
2. [Fonctionnalités](#fonctionnalités)
3. [Technologies Utilisées](#technologies-utilisées)
4. [Installation](#installation)
5. [Utilisation](#utilisation)
6. [Endpoints de l'API](#endpoints-de-lapi)
7. [Tests](#tests)
8. [Exemple avec Postman](#exemple-avec-postman)
9. [Structure du Projet](#structure-du-projet)

---

## Introduction

Cette API offre les fonctionnalités suivantes :
- Lister tous les films.
- Donner les détails d'un film spécifique, à partir de son titre ou du nom d'un acteur
- Mettre à jour les informations sur un film à partir de son titre.
- Renvoyer le nombre de films communs entre la base de données MongoDB et la base de données neo4j.
- Lister les utilisateurs qui ont évalué un film, à partir du titre d'un filtre.
- Retourner un utilisateur avec le nombre de films qu'il a notés et la liste des films notés, à partir du nom d'un utilisateur.

---

## Fonctionnalités

- **Intégration MongoDB** : Stockage et récupération des données liées aux films.
- **Intégration Neo4j** : Analyse des relations utilisateurs-films.
- **Exécution Locale** : L'application fonctionne sur votre machine.
- **API REST** : Points d'accès faciles à utiliser pour exploiter les fonctionnalités.

---

## Technologies Utilisées

- Python 3.8
- FastAPI
- MongoDB
- Neo4j
---

## Prérequis

- Avoir Python 3.8 (version minimum) installé sur votre machine.
- Avoir l'instance MongoDB avec la collection movies.
- Avoir l'instance Neo4j avec les relations nécessaires.
---

## Installation 

GIT ect ect

---

## Lancement 
1. Démarrez les serveurs **MongoDB** et **Neo4j** s'ils ne sont pas déjà en cours d'exécution.

2. Pour lancer l'application FastAPI, exécutez, en se plaçant dans le fichier contenant vos fichier .py :
```bash
python -m uvicorn main:app --reload
```
3. Visualisation de l'interface OpenAPI via :
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---
# Scénarios de test

### 1. Lister tous les films
- **Requête** : `GET /movies`
- **Données de test** : Aucune donnée spécifique n'est nécessaire. Ce scénario liste tous les films disponibles dans la base de données.

### 2. Rechercher un film par titre exact
- **Requête** : `GET /movies/search`
- **Données de test** : 
  - Titre du film : `Days of Thunder` (exemple d’un film de la liste obtenue à l'étape précédente).

### 3. Rechercher des films contenant un mot-clé dans le titre
- **Requête** : `GET /movies/search`
- **Données de test** : 
  - Mot-clé : `Days` ou `days` (exemple d’un mot du titre du film `Days of Thunder`).
  - Cela doit retourner tous les films dont le titre contient "days".

### 4. Rechercher des films par nom d’acteur
- **Requête** : `GET /movies/search`
- **Données de test** : 
  - Nom de l’acteur : `Tom Cruise` (exemple d'un acteur du casting dans la liste obtenue à l'étape 1).
  - Cela doit retourner tous les films dans lesquels `Tom Cruise` a joué.

### 5. Rechercher des films par nom ou prénom d'acteur
- **Requête** : `GET /movies/search`
- **Données de test** : 
  - Nom ou prénom de l’acteur : `Tom` ou `tom` OU `TOM` (exemple d’un acteur qui peut être trouvé sous ce prénom).

### 6. Rechercher un film par titre et acteur liés
- **Requête** : `GET /movies/search`
- **Données de test** : 
  - Titre du film : `Days of Thunder`
  - Nom de l’acteur : `Tom Cruise` (exemple de valeurs liées, où `Tom Cruise` joue dans `Days of Thunder`).
  - Cela doit afficher les détails du film `Days of Thunder` avec `Tom Cruise` dans le casting.

### 7. Rechercher un film par titre et acteur non liés
- **Requête** : `GET /movies/search`
- **Données de test** : 
  - Titre du film : `The Moon Is Blue`
  - Nom de l’acteur : `Tom Cruise` (exemple de valeurs non liées, où `Tom Cruise` ne joue pas dans `The Moon Is Blue`).
  - Aucun film ne doit être retourné.

### 8. Modifier un film
- **Requête** : `PUT /movies/{title}`
- **Données de test** : 
  - Titre du film : `The Moon Is Blue`
  - Corps de la requête pour la modification : 
    ```json
    {
      "plot": "string",
      "genres": ["test"],
      "cast": ["test"],
      "languages": ["test"],
      "directors": ["test"],
      "year": 2024
    }
    ```

### 9. Visualiser les modifications apportées
- **Requête** : `GET /movies/search`
- **Données de test** : 
  - Titre du film modifié : `The Moon Is Blue` (exemple du titre pour lequel les modifications ont été appliquées).

### 10. Connaître le nombre de films communs entre MongoDB et Neo4j
- **Requête** : `GET /movies/common-movies`

### 11. Lister les utilisateurs ayant évalué un film
- **Requête** : `GET /movies/movies/{title}/users`
- **Données de test** : 
  - Titre du film : `The Da Vinci Code` (vous pouvez entrer une partie du titre).

### 12. Lister les films notés par un utilisateur
- **Requête** : `GET /movies/users/{name}/rated-movies`
- **Données de test** : 
  - Nom de l’utilisateur : `Jessica Thompson` (vous pouvez entrer juste Thompson mais le résultat concerna tous les utilisateurs avec ce nom).
