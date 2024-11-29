#!/bin/bash

#!/bin/bash

# Étape 1 : Création des tables et insertion des données dans PostgreSQL
echo "Création des tables et insertion des données dans PostgreSQL..."
python config.py


# Étape 3 : Démarrage de l'application Streamlit
echo "Démarrage de l'application Streamlit..."
streamlit run streamlit_app.py
