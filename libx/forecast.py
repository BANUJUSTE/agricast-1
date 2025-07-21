import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

# Configuration du client avec cache et gestion des erreurs
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Paramètres de la requête météo
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 6.17,  # Exemple : Lomé, Togo
    "longitude": 1.21,
    "hourly": ["temperature_2m","wind_speed_10m","cloud_cover","relative_humidity_2m"]
}

# Appel à l’API
responses = openmeteo.weather_api(url, params=params)
response = responses[0]
# Traitement des données horaires
hourly = response.Hourly()
temperature = hourly.Variables(0).ValuesAsNumpy()
vent=hourly.Variables(1).ValuesAsNumpy()
humidite=hourly.Variables(3).ValuesAsNumpy()
nuage=hourly.Variables(2).ValuesAsNumpy()
dates = pd.date_range(
    start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
    end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
    freq=pd.Timedelta(seconds=hourly.Interval()),
    inclusive="left"
)

# Création du DataFrame
df = pd.DataFrame({
    "date": dates,
    "temperature_2m": temperature,
    "vent": vent,
    "nuage": nuage,
    "humidite": humidite
})
print(df.head())
