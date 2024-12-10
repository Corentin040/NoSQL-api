# API de Gestion des Films - Final Lab

Ce projet est une application Python permettant de gérer et d'analyser des données sur les films et les utilisateurs en utilisant les bases de données **MongoDB** et **Neo4j**. L'API REST, implémentée avec **Flask** ou **FastAPI**, permet de réaliser des opérations CRUD ainsi que des analyses croisées sur les données.

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
- Récupérer une liste de films.
- Rechercher un film ou un acteur.
- Mettre à jour les informations sur un film.
- Analyser les données communes entre MongoDB et Neo4j.
- Obtenir la liste des utilisateurs ayant noté un film.
- Récupérer les informations détaillées sur un utilisateur, y compris les films notés.

---

## Fonctionnalités

- **Intégration MongoDB** : Stockage et récupération des données liées aux films.
- **Intégration Neo4j** : Analyse des relations utilisateurs-films.
- **Exécution Locale** : L'application fonctionne sur votre machine.
- **API REST** : Points d'accès faciles à utiliser pour exploiter les fonctionnalités.

---

## Technologies Utilisées

- **Python 3.x**
- **Flask** / **FastAPI**
- **MongoDB**
- **Neo4j**
---

## Installation

### Prérequis

- Avoir Python 3.x installé sur votre machine.
- Installer MongoDB Community Edition : https://www.mongodb.com/try/download/community
- Installer Neo4j Desktop

### Étape 1 : Cloner le dépôt

```bash
git clone <url_du_dépôt>
cd <dossier_du_projet>
