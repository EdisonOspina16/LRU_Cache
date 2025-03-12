import time
import matplotlib.pyplot as plt
from API_PRUEBA import fetch_weather, fetch_weather_with_cache

def measure_performance(city, iterations=5):
    times_without_cache = []
    times_with_cache = []

    # Medir tiempos sin caché
    for _ in range(iterations):
        start_time = time.time()
        fetch_weather(city)
        elapsed_time = time.time() - start_time
        times_without_cache.append(elapsed_time)

    # Medir tiempos con caché
    for _ in range(iterations):
        start_time = time.time()
        fetch_weather_with_cache(city)
        elapsed_time = time.time() - start_time
        times_with_cache.append(elapsed_time)

    return times_without_cache, times_with_cache

def plot_performance(times_without_cache, times_with_cache):
    iterations = range(1, len(times_without_cache) + 1)
    plt.figure(figsize=(10, 5))
    plt.plot(iterations, times_without_cache, marker='o', linestyle='-', label='Sin caché')
    plt.plot(iterations, times_with_cache, marker='s', linestyle='-', label='Con caché')
    plt.xlabel('Número de iteración')
    plt.ylabel('Tiempo de respuesta (s)')
    plt.title('Comparación de tiempos de respuesta')
    plt.legend()
    plt.grid()
    plt.show()

def main():
    city = input("Ingrese la ciudad para medir el rendimiento: ").strip()
    times_without_cache, times_with_cache = measure_performance(city)
    plot_performance(times_without_cache, times_with_cache)

if __name__ == "__main__":
    main()
