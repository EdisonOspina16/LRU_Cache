# LRU Cache para API de Clima

Este proyecto implementa una caché LRU (Least Recently Used) para almacenar y recuperar datos del clima de la ciudad de Medellín utilizando la API de OpenWeather. El objetivo es mejorar la eficiencia al obtener el clima, evitando hacer solicitudes a la API repetidamente cuando los datos ya están disponibles en la caché.

## Descripción

El proyecto se basa en dos funcionalidades principales:

1. **Obtener el clima sin caché**: Realiza una solicitud directa a la API de OpenWeather.
2. **Obtener el clima con caché**: Usa una caché LRU para almacenar los datos obtenidos de la API. Si los datos ya están en la caché, no se realiza una nueva solicitud a la API y se obtienen de manera más rápida.

## Estructura del Proyecto

El proyecto tiene la siguiente estructura de archivos:


## Requisitos

Para ejecutar este proyecto, necesitas tener instalado lo siguiente:

- Python 3.12 o superior
- La biblioteca `requests` para realizar solicitudes HTTP.

Puedes instalar `requests` ejecutando el siguiente comando:

```bash
pip install requests
```
Además, necesitarás una clave de API de OpenWeather, que puedes obtener registrándote en su sitio web: OpenWeather.
Una vez que obtengas tu clave, guárdala en un archivo llamado ```secret_config.py``` con el siguiente formato:
```
API_KEY = 'tu_clave_de_api_aqui'
```

## Desarrolladores:
- Edison Ospina      --> [EdisonOspina16](https://github.com/EdisonOspina16)
- Juan Jose Cano     --> [Juanjosecano318](https://github.com/Juanjosecano318)
- Ximena Ruiz Arias  --> [Ximerza](https://github.com/ximerza)
- Steven             --> [JHONCE79](https://github.com/JHONCE79)
