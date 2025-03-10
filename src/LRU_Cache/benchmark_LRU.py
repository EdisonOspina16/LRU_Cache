import requests
import time
import statistics
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import secret_config
from src.LRU_Cache.LRUCache import LRUCache
import psutil

class CachePerformanceMetrics:
    def __init__(self, cache_capacity=2):
        self.cache = LRUCache(capacity=cache_capacity)
        self.cache_hits = 0
        self.cache_misses = 0
        self.api_response_times = []
        self.cache_response_times = []
        self.memory_usage = []  # Lista para almacenar uso de memoria
    
    def get_memory_usage(self):
        """Obtiene el uso actual de memoria en MB."""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / (1024 * 1024)  # Convertir a MB
    
    def fetch_weather(self, city):
        """
        Obtiene el clima sin caché y registra el tiempo de respuesta y memoria
        """
        memory_before = self.get_memory_usage()
        start_time = time.time()
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={secret_config.API_KEY}&units=metric"
        response = requests.get(url)
        
        end_time = time.time()
        memory_after = self.get_memory_usage()
        
        elapsed_time = end_time - start_time
        self.api_response_times.append(elapsed_time)
        self.memory_usage.append(memory_after - memory_before)

        if response.status_code == 200:
            data = response.json()
            print(f"[Sin caché] Clima en {city}: {data['weather'][0]['description']}, {data['main']['temp']}°C")
        else:
            print(f"Error en la solicitud: {response.status_code}")
            data = None

        print(f"Tiempo de respuesta sin caché: {elapsed_time:.4f} segundos")
        print(f"Uso de memoria sin caché: {memory_after - memory_before:.4f} MB")
        return data

    def fetch_weather_with_cache(self, city):
        """
        Intenta obtener datos del clima desde la caché y registra hits/misses, tiempo y memoria
        """
        memory_before = self.get_memory_usage()
        start_time = time.time()
        
        cached_data = self.cache.get(city)
        
        end_time = time.time()
        memory_after = self.get_memory_usage()
        
        elapsed_time = end_time - start_time
        self.memory_usage.append(memory_after - memory_before)
        
        if cached_data and isinstance(cached_data, dict):
            self.cache_hits += 1
            self.cache_response_times.append(elapsed_time)
            print(f"[Con caché] Clima en {city}: {cached_data['weather'][0]['description']}, {cached_data['main']['temp']}°C")
            print(f"Tiempo de respuesta con caché: {elapsed_time:.4f} segundos")
            print(f"Uso de memoria con caché: {memory_after - memory_before:.4f} MB")
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
        
        if self.memory_usage:
            print(f"\nUso promedio de memoria: {statistics.mean(self.memory_usage):.4f} MB")
            print(f"Uso máximo de memoria: {max(self.memory_usage):.4f} MB")
            print(f"Uso mínimo de memoria: {min(self.memory_usage):.4f} MB")
    
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

if __name__ == "__main__":
    cache_size = int(input("Ingrese el tamaño de la caché: "))
    metrics = CachePerformanceMetrics(cache_capacity=cache_size)
    
    test_cities = ["Madrid", "London", "New York", "Tokyo", "Madrid", "Paris", "London", "Berlin", "Madrid"]
    iterations = int(input("Ingrese el número de iteraciones para el test: "))
    metrics.run_performance_test(test_cities, iterations)
