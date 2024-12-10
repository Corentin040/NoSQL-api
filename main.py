from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as movies_router
from neo4j import GraphDatabase

import certifi
config = dotenv_values(".env")

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["MONGODB_URL"], tlsCAFile=certifi.where())
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")
    app.neo4j_driver = GraphDatabase.driver(config["NEO4J_URL"], auth=(config["NEO4J_USER"], config["NEO4J_PASSWORD"]))
    print("Connected to MongoDB and Neo4j databases!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    app.neo4j_driver.close()

app.include_router(movies_router, tags=["movies"], prefix="/movies")


