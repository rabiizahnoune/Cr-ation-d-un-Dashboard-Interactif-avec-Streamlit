from geopy.geocoders import Nominatim
import plotly.express as px
geolocator = Nominatim(user_agent="myGeocoder")

# Fonction pour obtenir la latitude et la longitude d'une ville
def get_coordinates(ville):
    location = geolocator.geocode(ville)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None
    

print(get_coordinates('MAROC'))
