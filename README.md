
# Projet Immobilier - Streamlit

Ce projet consiste en une application **Streamlit** pour la gestion des données immobilières. L'application permet de visualiser, filtrer, et analyser des données immobilières dans une interface interactive. Elle est déployée via un conteneur Docker et est prête à être exécutée sur une infrastructure cloud.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé les outils suivants :

- [Docker](https://www.docker.com/get-started) - Pour containeriser l'application.
- [Streamlit](https://streamlit.io/) - Framework Python pour la création d'applications web interactives.
- [Python 3.7+](https://www.python.org/downloads/) - Pour exécuter le code de l'application.

## Installation

### 1. Cloner le projet
Clonez ce dépôt sur votre machine locale :

```bash
git clone https://github.com/ton-compte/projet-immobilier.git
cd projet-immobilier
```

### 2. Créer et activer un environnement virtuel (facultatif mais recommandé)
Si vous préférez isoler les dépendances du projet, créez un environnement virtuel :

```bash
python -m venv .venv
source .venv/bin/activate  # Sur Linux/Mac
.venv\Scriptsctivate     # Sur Windows
```

### 3. Installer les dépendances
Installez les dépendances nécessaires à l'application :

```bash
pip install -r requirements.txt
```

### 4. Configuration Docker

Le projet est containerisé avec Docker. Voici les étapes pour préparer et exécuter l'application dans un conteneur.

#### a. Créer une image Docker

Dans le répertoire du projet, construisez l'image Docker :

```bash
docker-compose up .
```

#### b. Exécuter l'application avec Docker

Lancez l'application dans un conteneur Docker :

```bash
docker run -p 8501:8501 immobilier-app
```

Cela exposera l'application à l'adresse `http://localhost:8501`.
`
