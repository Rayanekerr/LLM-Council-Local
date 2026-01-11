#  LLM Council - Local Deployment Project

## Informations Générales

* **Étudiant :** Rayane KERROUCHE
* **Groupe TD :** CDOF3
* **Modalité :** Projet Solo

---

##  Project Overview

Ce projet est une implémentation locale du concept de **LLM Council**. Au lieu de s'appuyer sur un modèle unique, le système fait collaborer plusieurs Large Language Models (LLMs) qui répondent, critiquent et synthétisent une réponse finale.

L'intégralité du système tourne en local via **Ollama**, garantissant la confidentialité des données et l'absence de dépendance aux API cloud.

### Le flux de travail (3 Stages) :

1. **Stage 1 : First Opinions** : Deux modèles légers génèrent des réponses indépendantes à la requête.
2. **Stage 2 : Review & Ranking** : Chaque modèle analyse et critique anonymement les réponses de ses pairs.
3. **Stage 3 : Chairman Synthesis** : Un modèle "Président" plus puissant synthétise la question originale, les réponses et les critiques pour produire le résultat final.

---

##  Architecture du Système

Le système est conçu comme une architecture distribuée communiquant via des APIs REST, même lors d'une exécution sur une seule machine.

```text
       [ UTILISATEUR ] 
              |
              ▼
      +-----------------+
      |  Interface Web  | <---- (Streamlit UI)
      +-----------------+
              |
      ________|_________________________________________
     |        | (Requêtes REST API via localhost:11434) |
     |        ▼                                         |
     |  [ STAGE 1 : OPINIONS ]                          |
     |  - Llama 3.2 (1b) -------------------+           |
     |  - Phi 4 Mini ---------------------+ |           |
     |                                    | |           |
     |  [ STAGE 2 : REVIEW ]              | |           |
     |  - Modèles croisent leurs avis <---+ |           |
     |    (Anonymisation & Ranking)         |           |
     |                                      |           |
     |  [ STAGE 3 : CHAIRMAN ]              |           |
     |  - Llama 3.1 (8b) <------------------+           |
     |    (Synthèse finale des critiques)               |
     |__________________________________________________|
              |
              ▼
      [ RÉPONSE FINALE ]

```

---

## Setup and Installation Instructions

### 1. Installation d'Ollama

Téléchargez et installez Ollama depuis [ollama.com](https://ollama.com). Assurez-vous que l'application est lancée en arrière-plan.

### 2. Téléchargement des Modèles

Exécutez les commandes suivantes dans votre terminal pour installer les modèles utilisés par le conseil :

```bash
ollama pull llama3.2:1b
ollama pull phi4-mini
ollama pull llama3.1:8b

```

### 3. Configuration de l'environnement Python

Dans le dossier du projet :

```bash
# Création de l'environnement virtuel
python -m venv venv

# Activation (Windows)
venv\Scripts\activate

# Installation des dépendances
pip install requests streamlit

```

---

## Instructions to Run the Demo

1. Lancez le serveur Ollama.
2. Dans le dossier du projet, lancez l'application Streamlit :
```bash
streamlit run app.py

```


3. L'interface s'ouvrira automatiquement dans votre navigateur (`http://localhost:8501`).
4. **Test :** Saisissez une question (ex: "Avantages du déploiement Edge vs Cloud") et cliquez sur **"Lancer la délibération"**.
5. Naviguez entre les onglets pour inspecter les sorties intermédiaires.

---

## Short Technical Report

### Key Design Decisions

* **Communication REST :** Le système utilise des requêtes `POST` vers `http://localhost:11434/api/generate`. Ce choix permet de migrer facilement les modèles vers d'autres serveurs réseau.
* **Modularité :** La logique du conseil (`council_logic.py`) est séparée de l'interface utilisateur (`app.py`), facilitant la maintenance.
* **Performance locale :** Les appels aux LLM sont séquentiels pour éviter la saturation de la RAM lors de l'exécution sur une seule machine.

### Chosen LLM Models

* **Llama 3.2 (1b) & Phi 4 Mini :** Choisi pour le Stage 1 et 2 pour leur rapidité extrême et leur faible empreinte mémoire.
* **Llama 3.1 (8b) :** Utilisé comme **Chairman**. Sa plus grande taille de paramètres permet une synthèse nuancée et une meilleure compréhension des critiques.

### Improvements made over the original repository

* **Indicateur de Santé :** Ajout d'un "Health Check" dynamique dans la barre latérale pour vérifier la connexion à Ollama.
* **Interface à Onglets :** Organisation claire des résultats par étape (Opinions / Critiques / Synthèse) pour une meilleure inspection.
* **Panneaux Repliables :** Utilisation d'expanders pour les critiques afin d'améliorer la lisibilité.

---

## Generative AI Usage Statement

J'ai utilisé l'IA **Gemini (Google)** pour :

* Aider à la conception de l'architecture distribuée.
* Aider pour le code de base pour l'interface Streamlit.


