import requests
import time
import secret_config


# Configuración
CITY = "Medellin"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={secret_config.API_KEY}&units=metric"


# Medir tiempo sin caché
start_time = time.time()
response = requests.get(URL)
end_time = time.time()

# Calcular tiempo de respuesta
elapsed_time = end_time - start_time

if response.status_code == 200:
    data = response.json()

    print(f"Clima en Medellín: {data['weather'][0]['description']},{data['main']['temp']}°C,")
else:
    print(f"Error en la solicitud: {response.status_code}")

print(f"Tiempo de respuesta sin caché: {elapsed_time:.4f} segundos")


# medir el tiempo con la cache
def fetch_weather_with_cache():
    pass