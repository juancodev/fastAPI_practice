# ⚡ FastAPI Practice

Este repositorio está enfocado en mostrarte los conceptos básico sobre [FastAPI]('https://fastapi.tiangolo.com/') y explicando paso a paso cómo poder iniciar con este **framework**.

## ¿Qué es FastAPI?

> FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.8+ based on standard Python type hints.

## 🐍 Primeros pasos:

- Haz clone o fork de este repositorio.
- Moverse a la carpeta `cd fastAPI_practice`
- Crea un entorno virtual `python3 -m venv "nombre del entorno virtual sin las comillas"`.
- Activa el entorno virtual con **shell** `$source "nombre del entorno virtual"/bin/activate`
- Instala los paquetes y dependencia `pip3 install -r requirements.txt`
- Activar el servidor local `uvicorn main:app --reload --port 5050 --host 0.0.0.0`
- Ingresa en tu navegador al [http://0.0.0.0:5050](http://0.0.0.0:5050), asegúrate que tengas activo uvicorn.

## 🌐 Rutas:

- **/**: Raíz del proyecto
- **/docs** : documentación en Swagger de la API
- **/movies**: Lista de películas en formato JSON.
- **/movies/id**: El id debe ser un número y te mostrará solamente esa película.
- **/movies/?category=nombre_de_la_categoria**: Te mostrará la película depende de su categoría.

### Interés:

Si te gustaría contribuir con alguna mejora de la API es totalmente válido.
