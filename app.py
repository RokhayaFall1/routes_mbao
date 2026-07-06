import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import pandas as pd

# =========================================================
# 1. CONFIGURATION DE LA PAGE WEB
# =========================================================
st.set_page_config(
    page_title="Webmapping - Projet Intégrateur Mbao", 
    layout="wide"
)

# =========================================================
# 2. CHARGEMENT OPTIMISÉ DES DONNÉES
# =========================================================
@st.cache_data
def charger_donnees_mbao():
    commune = gpd.read_file("commune_mbao.geojson")
    quartiers = gpd.read_file("quartiers.geojson")  
    routes = gpd.read_file("reseau_routier.geojson")
    route_inondable = gpd.read_file("route_inondable.geojson")
    route_priorite2 = gpd.read_file("route_priorite2.geojson")
    route_urgence = gpd.read_file("route_urgence_absolu.geojson")
    zone_risque = gpd.read_file("zone_a_risque.geojson")
    rond_point = gpd.read_file("rondpoint.geojson")
    autopont = gpd.read_file("autopont.geojson")
    train = gpd.read_file("train.geojson")
            
    return (commune, quartiers, routes, route_inondable, route_priorite2, route_urgence,
            zone_risque, rond_point, autopont, train)

# Instanciation des données
(commune, quartiers, routes, route_inondable, route_priorite2, route_urgence,
 zone_risque, rond_point, autopont, train) = charger_donnees_mbao()

# =========================================================
# 3. STRUCTURATION DE L'INTERFACE EN COLONNES (40% / 60%)
# =========================================================
col1, col2 = st.columns([1, 1.5])

# =========================================================
# COLONNE 1 : PANNEAU DE CONTROLE ET FILTRES (À GAUCHE)
# =========================================================
with col1:
    st.header("📊 Gestion des Couches")
    
    st.subheader("🗺️ Données de Base & Communes")
    afficher_commune = st.checkbox("Limite Communale (Mbao)", value=True)
    afficher_quartiers = st.checkbox("Quartiers de Mbao", value=False)  
    afficher_routes = st.checkbox("Réseau routier global (Noir)", value=True)
    
    st.subheader("⚠️ Risques & Vulnérabilité")
    afficher_zone_risque = st.checkbox("Zones à risque d'inondation (Bleu)", value=True)
    afficher_route_inondable = st.checkbox("Tronçons routiers inondables", value=True)
    
    st.subheader("🚨 Infrastructures & Priorités d'Intervention")
    afficher_priorite2 = st.checkbox("Routes - Priorité 2 (Secondaire)", value=False)
    afficher_urgence = st.checkbox("Routes - Urgence Absolue", value=True)
    afficher_autopont = st.checkbox("📍 Afficher l'Autopont (Rose)", value=True)
    afficher_rond_point = st.checkbox("⭕ Afficher le Rond-point (Violet)", value=True)
    afficher_train = st.checkbox("🛤️ Ligne de Train (TER)", value=True)
    
    st.write("---")
    st.info("💡 Utilisez les filtres ci-dessus pour activer ou masquer les éléments de votre diagnostic territorial.")

# =========================================================
# COLONNE 2 : CARTE INTERACTIVE (À DROITE)
# =========================================================
with col2:
    st.header("🗺️ Visualisation Cartographique")
    
    # Centre de la carte calé sur la commune de Mbao
    centre_mbao = [14.740, -17.323]
    m = folium.Map(location=centre_mbao, zoom_start=13.5, tiles="OpenStreetMap")
    
    # 1. Zones à risque d'inondation (Couleur Bleue)
    if afficher_zone_risque and not zone_risque.empty:
        folium.GeoJson(
            zone_risque,
            name="Zones à risque",
            style_function=lambda x: {
                'fillColor': '#0000FF', 
                'color': '#00008B',     
                'weight': 1.5, 
                'fillOpacity': 0.4
            }
        ).add_to(m)
        
    # 2. Ajout de la couche Quartiers
    if afficher_quartiers and not quartiers.empty:
        folium.GeoJson(
            quartiers,
            name="Quartiers",
            style_function=lambda x: {
                'color': '#ffa500', 
                'weight': 1.5, 
                'fillOpacity': 0.02, 
                'dashArray': '5, 5'
            }
        ).add_to(m)

    # 3. Limite Communale
    if afficher_commune and not commune.empty:
        folium.GeoJson(
            commune,
            name="Limite Communale",
            style_function=lambda x: {'color': '#333333', 'weight': 3, 'fillColor': 'none'}
        ).add_to(m)

    # 4. Réseau Routier Global (Couleur Noire)
    if afficher_routes and not routes.empty:
        folium.GeoJson(
            routes,
            name="Réseau Routier Global",
            style_function=lambda x: {'color': '#000000', 'weight': 1.2, 'opacity': 0.7}
        ).add_to(m)

    # 5. Tronçons de routes inondables
    if afficher_route_inondable and not route_inondable.empty:
        folium.GeoJson(
            route_inondable,
            name="Routes Inondables",
            style_function=lambda x: {'color': '#0000ff', 'weight': 3.5, 'opacity': 0.8, 'dashArray': '3, 4'}
        ).add_to(m)

    # 6. Routes - Priorité 2
    if afficher_priorite2 and not route_priorite2.empty:
        folium.GeoJson(
            route_priorite2,
            name="Routes - Priorité 2",
            style_function=lambda x: {'color': '#ffaa00', 'weight': 2.5, 'opacity': 0.8}
        ).add_to(m)

    # 7. Routes - Urgence Absolue
    if afficher_urgence and not route_urgence.empty:
        folium.GeoJson(
            route_urgence,
            name="Urgence Absolue",
            style_function=lambda x: {'color': '#e31a1c', 'weight': 4.5, 'opacity': 1.0}
        ).add_to(m)

    # 8. Tracé Ferroviaire (Train)
    if afficher_train and not train.empty:
        folium.GeoJson(
            train,
            name="Ligne Ferroviaire",
            style_function=lambda x: {'color': '#4a4a4a', 'weight': 3, 'dashArray': '6, 4', 'opacity': 0.9}
        ).add_to(m)

    # 9. Structure de l'Autopont
    if afficher_autopont and not autopont.empty:
        folium.GeoJson(
            autopont,
            name="Autopont",
            style_function=lambda x: {
                'color': '#ff00ff', 
                'weight': 5, 
                'fillColor': '#ff00ff', 
                'fillOpacity': 0.7
            },
            marker=folium.CircleMarker(radius=8, color='#ff00ff', fillColor='#ff00ff', fillOpacity=0.8)
        ).add_to(m)

    # 10. Rond-point
    if afficher_rond_point and not rond_point.empty:
        folium.GeoJson(
            rond_point,
            name="Rond-point",
            style_function=lambda x: {
                'color': '#800080', 
                'weight': 5, 
                'fillColor': '#800080', 
                'fillOpacity': 0.7
            },
            marker=folium.CircleMarker(radius=9, color='#800080', fillColor='#800080', fillOpacity=0.9)
        ).add_to(m)

    # Rendu final de la carte dans l'application Streamlit
    st_folium(m, width=850, height=600, returned_objects=[])
