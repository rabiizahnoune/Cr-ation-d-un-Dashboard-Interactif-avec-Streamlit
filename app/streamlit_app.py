import streamlit as st
import pandas as pd
import plotly.express as px

import folium
from folium.plugins import MarkerCluster
from sqlalchemy import create_engine
import numpy as np
from db import df_orm,df_orm_equipement
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

st.set_page_config(page_title="Analyse des Annonces Immobilières", layout="wide")
st.title("Analyse des Annonces Immobilières")


# Load data from ORM
df = pd.DataFrame(df_orm, columns=[
    'id', 'title', 'price', 'datetime', 'nb_rooms', 'nb_baths', 
    'surface_area', 'name', 'longitude', 'latitude'
])

df["price"] = pd.to_numeric(df['price'], errors='coerce')

# Page selection in sidebar
page = st.sidebar.selectbox("Sélectionnez une page", ["Page de filtrage des données", "Page de visualisation", "Carte des annonces"])

if page == "Page de filtrage des données":
    st.write("### Filtrage des données")
    st.write("Sur cette page, vous pouvez filtrer les données selon plusieurs critères.")
    
    min_prix, max_prix = st.sidebar.slider("Sélectionnez la plage de prix", min_value=0, max_value=1000000, value=(100000, 500000))
    min_surface, max_surface = st.sidebar.slider("Sélectionnez la plage de surface (m²)", min_value=50, max_value=400, value=(50, 150))
    min_rooms, max_rooms = st.sidebar.slider('Sélectionner le nombre de chambres', min_value=df['nb_rooms'].min(), max_value=df['nb_rooms'].max(), value=(1, 5))
    villes = df['name'].unique() 
    villes_options = ['Tous'] + list(villes)
    selected_villes = st.sidebar.multiselect("Sélectionnez une ou plusieurs villes", options=villes_options)

    # Filter data based on user selections
    if 'Tous' in selected_villes:
        filtered_df = df[
            (df['price'] >= min_prix) &
            (df['price'] <= max_prix) &
            (df['surface_area'] >= min_surface) &
            (df['surface_area'] <= max_surface) &
            (df['nb_rooms'] >= min_rooms) &
            (df['nb_rooms'] <= max_rooms)
        ]
    else:
        filtered_df = df[
            (df['price'] >= min_prix) &
            (df['price'] <= max_prix) &
            (df['surface_area'] >= min_surface) &
            (df['surface_area'] <= max_surface) &
            (df['nb_rooms'] >= min_rooms) &
            (df['nb_rooms'] <= max_rooms) &
            (df['name'].isin(selected_villes))
        ]
    
    st.write(f"**Résultats filtrés** : {filtered_df.shape[0]} annonces correspondantes.")
    st.write(filtered_df)

elif page == "Page de visualisation":
    st.write("### Visualisation des graphiques")
    st.write("Sur cette page, vous pouvez visualiser différents graphiques basés sur les données filtrées ou toutes les données.")
    view_option = st.sidebar.radio("Que voulez-vous visualiser ?", ["Toutes les données", "Données filtrées"])

    if view_option == "Données filtrées":
        st.write("### Filtres")
        min_prix, max_prix = st.sidebar.slider("Sélectionnez la plage de prix", min_value=0, max_value=1000000, value=(100000, 500000))
        min_surface, max_surface = st.sidebar.slider("Sélectionnez la plage de surface (m²)", min_value=50, max_value=400, value=(50, 150))
        min_rooms, max_rooms = st.sidebar.slider('Sélectionner le nombre de chambres', min_value=df['nb_rooms'].min(), max_value=df['nb_rooms'].max(), value=(1, 5))
        
        villes = df['name'].unique() 
        villes_options = ['Tous'] + list(villes)  
        selected_villes = st.sidebar.multiselect("Sélectionnez une ou plusieurs villes", options=villes_options)

        # Apply filters to the data
        if 'Tous' in selected_villes:
            filtered_df = df[
                (df['price'] >= min_prix) &
                (df['price'] <= max_prix) &
                (df['surface_area'] >= min_surface) &
                (df['surface_area'] <= max_surface) &
                (df['nb_rooms'] >= min_rooms) &
                (df['nb_rooms'] <= max_rooms)
            ]
        else:
            filtered_df = df[
                (df['price'] >= min_prix) &
                (df['price'] <= max_prix) &
                (df['surface_area'] >= min_surface) &
                (df['surface_area'] <= max_surface) &
                (df['nb_rooms'] >= min_rooms) &
                (df['nb_rooms'] <= max_rooms) &
                (df['name'].isin(selected_villes))
            ]
        st.write(f"**Résultats filtrés** : {filtered_df.shape[0]} annonces correspondantes.")
        st.write(filtered_df)
    else:
        filtered_df = df  
        st.write(f"**Toutes les données** : {filtered_df.shape[0]} annonces au total.")
        st.write(filtered_df)

    # Create a row of two columns for the first two graphs
    col1, col2 = st.columns(2)

    with col1:
        # Price distribution plot
        fig_prix = px.histogram(
            filtered_df,
            x="price",
            nbins=30,
            title="Distribution des prix",
            labels={"price": "Prix"},
            color_discrete_sequence=["skyblue"]
        )
        fig_prix.update_traces(opacity=0.75)
        fig_prix.update_layout(
            title=dict(x=0.5),
            xaxis=dict(
                title="Prix (en MAD)", 
                tickprefix="MAD ", 
                showgrid=False
            ),
            yaxis=dict(
                title="Nombre d'annonces",
                showgrid=True,
            ),
            template="plotly_white",
            font=dict(size=14),
            margin=dict(l=40, r=40, t=80, b=40),
            bargap=0.2
        )
        st.plotly_chart(fig_prix)

    with col2:
        # City distribution plot
        city_counts = df['name'].value_counts().reset_index() 
        city_counts.columns = ['Ville', 'Nombre d\'annonces']
        top_n = 10
        city_counts = city_counts.head(top_n)

        fig_ville = px.bar(
            city_counts,
            x='Ville',
            y='Nombre d\'annonces',
            title='Distribution des annonces par ville',
            labels={"Nombre d\'annonces": "Nombre d'annonces", "Ville": "Ville"},
            text='Nombre d\'annonces',
            color='Nombre d\'annonces',
            color_continuous_scale='Blues'
        )
        fig_ville.update_traces(
            texttemplate='%{text}', 
            textposition='outside'
        )
        fig_ville.update_layout(
            xaxis=dict(categoryorder='total descending'),
            title=dict(x=0.5),
            template='plotly_white'
        )
        st.plotly_chart(fig_ville)

    # Create another row of two columns for the next two graphs
    col3, col4 = st.columns(2)

    with col3:
        # Equipment distribution plot
        df_equipement = pd.DataFrame(df_orm_equipement, columns=['equipement', 'nombre_annonces'])
        fig_equipement = px.pie(
            df_equipement, 
            names='equipement', 
            values='nombre_annonces',
            title="Répartition des équipements dans les annonces immobilières",
            labels={'equipement': 'Équipement', 'nombre_annonces': 'Nombre d\'annonces'},
            color='nombre_annonces',
            color_discrete_sequence=px.colors.sequential.Blues,
            hole=0.3
        )
        st.plotly_chart(fig_equipement, use_container_width=True)

    with col4:
        # Price vs. Surface plot
        fig_price_area = px.scatter(
            df,
            x='surface_area',
            y='price',
            color='name',
            size='surface_area',
            hover_data=['name'],
            labels={
                'surface_area': "Surface (m²)",
                'price': "Prix (MAD)",
            },
            title="Relation entre la surface et le prix des biens"
        )
        fig_price_area.update_traces(marker=dict(opacity=0.7, line=dict(width=1, color='DarkSlateGrey')))
        fig_price_area.update_layout(
            title_font=dict(size=20, family='Arial'),
            xaxis_title="Surface (m²)",
            yaxis_title="Prix (MAD)",
            legend_title="name",
            template='plotly_white'
        )
        st.plotly_chart(fig_price_area)

    # Create another row of two columns for the last two graphs
    col5, col6 = st.columns(2)

    with col5:
        # Room vs. Price plot
        fig_room_price = px.box(
            df, 
            x='nb_rooms', 
            y='price', 
            title="Distribution des prix selon le nombre de chambres",
            labels={'nb_rooms': 'Nombre de chambres', 'price': 'Prix'},
            color='nb_rooms',
            
        )
        fig_room_price.update_layout(
            boxmode='group',
            title=dict(x=0.5),
            xaxis=dict(title="Nombre de chambres"),
            yaxis=dict(title="Prix (MAD)"),
            template='plotly_white'
        )
        st.plotly_chart(fig_room_price)

    with col6:
        # Surface vs. Price plot
        
       df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

       df['month'] = df['datetime'].dt.to_period('M').astype(str)


       annonces_par_mois = df.groupby('month').size().reset_index(name='nombre_annonces')


       fig = px.line(
    annonces_par_mois,
    x='month',
    y='nombre_annonces',
    title="Évolution du nombre d'annonces publiées au fil du temps",
    labels={'month': 'Mois', 'nombre_annonces': 'Nombre d\'annonces'},
    line_shape='linear', 
    markers=True,        
    line_dash_sequence=["solid"], 
    color_discrete_sequence=px.colors.sequential.Blues  
)

       st.plotly_chart(fig)

    col7, col8 = st.columns(2)

    with col7:
         moyennes = df.groupby('name')[['nb_rooms', 'nb_baths']].mean().reset_index()
         fig = px.bar(
    moyennes,
    x='name', 
    y=['nb_rooms', 'nb_baths'], 
    title="Nombre moyen de pièces et de salles de bain par ville",
    labels={'name': 'Ville', 'value': 'Nombre moyen'},
    barmode='group',  
    color_discrete_sequence=['#3498db', '#e74c3c'], 
)


         st.plotly_chart(fig)

    
elif page == "Carte des annonces":
    unique_villes = df['name'].unique()  # Villes uniques



# Obtenir les coordonnées pour chaque ville unique
    
    fig_map = px.scatter_mapbox(
    df,
    lat="latitude",
    lon="longitude", # Affichage de l'info sur l'annonce
    hover_data=["name"],   # Afficher le nom de la ville
    title="Localisation des annonces immobilières",
    color="name",  # Coloration par ville (colonne 'name')
    color_discrete_sequence=px.colors.qualitative.Set1
)

# Configurer la carte
    fig_map.update_layout(
    mapbox_style="carto-positron",  # Style de la carte
    mapbox_zoom=5,  # Niveau de zoom
    mapbox_center={"lat": 28.3347722, "lon": -10.371337908392647},  # Centre de la carte (en France ici)
)

# Afficher la carte dans Streamlit
    st.plotly_chart(fig_map)

