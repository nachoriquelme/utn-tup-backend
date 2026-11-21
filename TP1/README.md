# TP1: ABM de Usuarios con FastAPI + ABM propio

Esta aplicación implementa una API REST con FastAPI y validación de datos con Pydantic, permitiendo realizar operaciones completas de Alta, Baja, Modificación y Consulta (ABM / CRUD) en memoria para las entidades Usuarios y Productos.

## Estructura del proyecto

TP1/
│
├── models/                  # Modelos de datos y esquemas Pydantic
│   ├── __init__.py
│   ├── users.py             # Esquemas para la entidad Usuario
│   └── productos.py         # Esquemas para la entidad Producto
│
├── routers/                 # Definición de rutas y lógica de los endpoints
│   ├── __init__.py
│   ├── users.py             # Endpoints ABM de Usuarios (/users)
│   └── productos.py         # Endpoints ABM de Productos (/products)
│
├── main.py                  # Punto de entrada de la aplicación FastAPI
├── requirements.txt         # Dependencias del proyecto
└── README.md                # Documentación e instrucciones de uso


## Como correrlo

## Clonar el repositorio

```bash
git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
cd tu-repositorio
```

## Crear el entorno virtual (venv)

Desde esta carpeta (`TP1`):

```bash
python3 -m venv .venv
```
Activar el entorno virtual:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

## Instalar los requerimientos

Con el entorno virtual activado:

```bash
pip install -r requirements.txt
```

## Ejecutar la aplicación:

```bash
fastapi dev main.py
```

La API quedará disponible en `http://127.0.0.1:8000` y la documentación interactiva (Swagger UI) en `http://127.0.0.1:8000/docs`.

Para probar los endpoints desde Swagger, haz clic sobre cualquiera de las rutas desplegadas (GET, POST, PUT, DELETE) para expandirla. Mediante el botón "Try it out" ubicado a la derecha, podras completar los parámetros o el cuerpo JSON requerido (en caso de POST o PUT). Presionando "Execute" podras enviar la petición y observar el código de respuesta HTTP y los datos devueltos.
