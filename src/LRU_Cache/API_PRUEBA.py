import requests
import time 
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import secret_config
from src.LRU_Cache.LRUCache import LRUCache

# Crear caché con capacidad para n entradas
cache = LRUCache(capacity=2)

def fetch_weather(city):
    """
    Obtiene el clima sin caché
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={secret_config.API_KEY}&units=metric"
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()
    elapsed_time = end_time - start_time

    if response.status_code == 200:
        data = response.json()
        print(f"[Sin caché] Clima en {city}: {data['weather'][0]['description']}, {data['main']['temp']}°C")
    else:
        print(f"Error en la solicitud: {response.status_code}")
        data = None  # Asegurar que data sea None si hay error

    print(f"Tiempo de respuesta sin caché: {elapsed_time:.4f} segundos")
    return data

def fetch_weather_with_cache(city):
    start_time = time.time()
    cached_data = cache.get(city)
    end_time = time.time()
    elapsed_time = end_time - start_time

    if cached_data and isinstance(cached_data, dict):
        print(f"[Con caché] Clima en {city}: {cached_data['weather'][0]['description']}, {cached_data['main']['temp']}°C")
        print(f"Tiempo de respuesta con caché: {elapsed_time:.4f} segundos")
        return cached_data



    print("[INFO] No se encontraron datos en caché. Haciendo solicitud a la API...")
    data = fetch_weather(city)
    if isinstance(data, dict):
        cache.put(city, data)
        print("[INFO] Datos almacenados en caché.")
    else:
        print("[ERROR] Los datos recibidos no son válidos.")

    return data

def main():
    while True:
        city = input("Ingrese el nombre de una ciudad para consultar el clima (o 'salir' para terminar): ").strip()
        if city.lower() == 'salir':
            print("Saliendo del programa...")
            break
        fetch_weather_with_cache(city)

if __name__ == "__main__":
    main()