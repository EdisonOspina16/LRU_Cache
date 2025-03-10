import requests
import time
import statistics
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import secret_config
from src.LRU_Cache.LRUCache import LRUCache

class CachePerformanceMetrics:
    def __init__(self, cache_capacity=2):
        self.cache = LRUCache(capacity=cache_capacity)
        self.cache_hits = 0
        self.cache_misses = 0
        self.api_response_times = []
        self.cache_response_times = []
        
    def fetch_weather(self, city):
        """
        Obtiene el clima sin caché y registra el tiempo de respuesta
        """
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={secret_config.API_KEY}&units=metric"
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()
        elapsed_time = end_time - start_time
        self.api_response_times.append(elapsed_time)

        if response.status_code == 200:
            data = response.json()
            print(f"[Sin caché] Clima en {city}: {data['weather'][0]['description']}, {data['main']['temp']}°C")
        else:
            print(f"Error en la solicitud: {response.status_code}")
            data = None

        print(f"Tiempo de respuesta sin caché: {elapsed_time:.4f} segundos")
        return data

    def fetch_weather_with_cache(self, city):
        """
        Intenta obtener datos del clima desde la caché y registra hits/misses
        """
        start_time = time.time()
        cached_data = self.cache.get(city)
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        if cached_data and isinstance(cached_data, dict):
            self.cache_hits += 1
            self.cache_response_times.append(elapsed_time)
            print(f"[Con caché] Clima en {city}: {cached_data['weather'][0]['description']}, {cached_data['main']['temp']}°C")
            print(f"Tiempo de respuesta con caché: {elapsed_time:.4f} segundos")
            return cached_data

        print("[INFO] No se encontraron datos en caché. Haciendo solicitud a la API...")
        self.cache_misses += 1
        data = self.fetch_weather(city)
        
        if isinstance(data, dict):
            self.cache.put(city, data)
            print("[INFO] Datos almacenados en caché.")
        else:
            print("[ERROR] Los datos recibidos no son válidos.")

        return data
    
    def print_performance_metrics(self):
        """
        Muestra las métricas de rendimiento acumuladas
        """
        total_requests = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total_requests) * 100 if total_requests > 0 else 0
        
        print("\n===== MÉTRICAS DE RENDIMIENTO =====")
        print(f"Total de solicitudes: {total_requests}")
        print(f"Cache hits: {self.cache_hits}")
        print(f"Cache misses: {self.cache_misses}")
        print(f"Hit rate: {hit_rate:.2f}%")
        
        if self.api_response_times:
            print(f"\nTiempo promedio de respuesta API: {statistics.mean(self.api_response_times):.4f} segundos")
            print(f"Tiempo máximo de respuesta API: {max(self.api_response_times):.4f} segundos")
            print(f"Tiempo mínimo de respuesta API: {min(self.api_response_times):.4f} segundos")
        
        if self.cache_response_times:
            print(f"\nTiempo promedio de respuesta caché: {statistics.mean(self.cache_response_times):.4f} segundos")
            print(f"Tiempo máximo de respuesta caché: {max(self.cache_response_times):.4f} segundos")
            print(f"Tiempo mínimo de respuesta caché: {min(self.cache_response_times):.4f} segundos")
            
            if self.api_response_times:
                avg_api = statistics.mean(self.api_response_times)
                avg_cache = statistics.mean(self.cache_response_times)
                speedup = (avg_api / avg_cache) if avg_cache > 0 else 0
                print(f"\nAceleración promedio con caché: {speedup:.2f}x")
    
    def run_performance_test(self, cities, iterations=2):
        """
        Ejecuta un test de rendimiento con una lista de ciudades
        """
        print(f"Iniciando prueba de rendimiento con {len(cities)} ciudades y {iterations} iteraciones...\n")
        
        for i in range(iterations):
            print(f"\n----- Iteración {i+1} -----")
            for city in cities:
                self.fetch_weather_with_cache(city)
                
        self.print_performance_metrics()

def main():
    # Crear instancia de métricas con capacidad de caché personalizable
    cache_size = int(input("Ingrese el tamaño de la caché: "))
    metrics = CachePerformanceMetrics(cache_capacity=cache_size)
    
    # Opción 1: Test automático
    print("\n1. Test automático con ciudades predefinidas")
    print("2. Test manual (ingresar ciudades)")
    choice = input("Seleccione una opción (1/2): ")
    
    if choice == "1":
        # Lista de ciudades para prueba automática
        test_cities = ["Madrid", "London", "New York", "Tokyo", "Madrid", "Paris", "London", "Berlin", "Madrid"]
        iterations = int(input("Ingrese el número de iteraciones para el test: "))
        metrics.run_performance_test(test_cities, iterations)
    else:
        # Modo manual similar al script original
        while True:
            city = input("\nIngrese el nombre de una ciudad para consultar el clima (o 'salir' para terminar): ").strip()
            if city.lower() == 'salir':
                print("Generando métricas finales...")
                metrics.print_performance_metrics()
                print("Saliendo del programa...")
                break
            metrics.fetch_weather_with_cache(city)

if __name__ == "__main__":
    main()