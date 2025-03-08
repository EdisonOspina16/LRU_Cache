import requests
import time
import secret_config
from src.LRU_Cache.LRUCache import LRUCache

# Configuración
CITY = "Medellin"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={secret_config.API_KEY}&units=metric"

# Crear caché con capacidad para 5 entradas
cache = LRUCache(capacity=5)


def fetch_weather():
    """Obtiene el clima sin caché"""
    start_time = time.time()
    response = requests.get(URL)
    end_time = time.time()
    elapsed_time = end_time - start_time

    if response.status_code == 200:
        data = response.json()
        print(f"[Sin caché] Clima en Medellín: {data['weather'][0]['description']}, {data['main']['temp']}°C")
    else:
        print(f"Error en la solicitud: {response.status_code}")
        data = None  # Asegurar que data sea None si hay error

    print(f"Tiempo de respuesta sin caché: {elapsed_time:.4f} segundos")
    return data


def fetch_weather_with_cache():
    #Verifica si el clima está en caché antes de hacer la solicitud
    print("[INFO] Intentando obtener datos de la caché...")

    cached_data = cache.get(CITY)
    print(f"[DEBUG] Cache content: {cached_data}")  # Depuración

    if cached_data and isinstance(cached_data, dict):
        start_time = time.time()  # Inicia el cronómetro
        result = cached_data  # Obtiene los datos de la caché
        end_time = time.time()  # Detiene el cronómetro

        elapsed_time = end_time - start_time  # Calcula el tiempo transcurrido

        print(f"[Con caché] Clima en Medellín: {result['weather'][0]['description']}, {result['main']['temp']}°C")
        print(f"Tiempo de respuesta con caché: {elapsed_time:.6f} segundos")  # Imprime el tiempo real
        return result

    print("[INFO] No se encontraron datos en caché. Haciendo solicitud a la API...")

    # Si no está en caché, hacer la solicitud
    data = fetch_weather()
    if isinstance(data, dict):  # Asegurar que los datos sean correctos antes de guardarlos
        cache.put(CITY, data)
        print("[INFO] Datos almacenados en caché.")
    else:
        print("[ERROR] Los datos recibidos no son válidos.")

    return data


# 🚀 PRUEBAS
print("🔵 Ejecutando sin caché:")
fetch_weather()  # Primera vez sin caché

print("\n🟢 Ejecutando con caché (primera vez, debe hacer la solicitud):")
fetch_weather_with_cache()  # Guarda en caché

print("\n🟢 Ejecutando con caché (segunda vez, debe devolver instantáneo):")
fetch_weather_with_cache()  # Usa la caché
