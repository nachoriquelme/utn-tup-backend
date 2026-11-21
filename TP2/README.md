# TP2: Sistema de Biblioteca — API REST (FastAPI + SQLModel)

API REST para gestionar el catálogo de libros y autores, socios, préstamos, devoluciones y control de roles (`bibliotecario` y `socio`), desarrollada con **FastAPI** y **SQLModel**.

## Estructura del Proyecto

```text
biblioteca-api/
├── auth.py
├── database.py
├── main.py
├── requirements.txt
├── README.md
├── models/
│   ├── __init__.py
│   ├── autor.py
│   ├── libro.py
│   ├── libro_autor.py
│   ├── prestamo.py
│   └── socio.py
├── routers/
│   ├── __init__.py
│   ├── autores.py
│   ├── libros.py
│   ├── prestamos.py
│   └── socios.py
├── services/
│   ├── __init__.py
│   ├── autor_service.py
│   ├── libro_service.py
│   ├── prestamo_service.py
│   └── socio_service.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_autores.py
    ├── test_database.py
    ├── test_libros.py
    ├── test_prestamos.py
    ├── test_roles.py
    └── test_socios.py
```

## Como correrlo

Se recomienda utilizar **Python 3.12 o 3.13** en el entorno virtual para evitar conflictos de compatibilidad entre versiones recientes de Python y los paquetes ORM/validación.

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
*(También podés ejecutarlo con `uvicorn main:app --reload`.)*

La API quedará disponible en `http://127.0.0.1:8000` y la documentación interactiva (Swagger UI) en `http://127.0.0.1:8000/docs`.


## Roles y Autenticación por Headers

La API valida el acceso mediante headers HTTP:

- **`X-Role: bibliotecario`**: puede administrar el catálogo (`/autores`, `/libros`, asociación de autores a libros), gestionar socios y registrar préstamos o devoluciones.
- **`X-Role: socio`** + **`X-Socio-Id: <id>`**: puede consultar el catálogo y ver **únicamente sus propios préstamos** en `/socios/{id}/prestamos`.

Ejemplo de petición como bibliotecario:
```http
GET /libros?disponibles=true
X-Role: bibliotecario
```

Ejemplo de petición como socio:
```http
GET /socios/1/prestamos?activos=true
X-Role: socio
X-Socio-Id: 1
```

## Endpoints Principales

| Método | Ruta | Descripción | Roles permitidos |
|---|---|---|---|
| `CRUD` | `/autores` | Alta, consulta, modificación y baja de autores | Lectura: ambos / Escritura: `bibliotecario` |
| `CRUD` | `/libros` | Alta, consulta, modificación y baja de libros | Lectura: ambos / Escritura: `bibliotecario` |
| `POST` | `/libros/{id}/autores/{autor_id}` | Asocia un autor a un libro ($N:N$) | `bibliotecario` |
| `GET` | `/libros?disponibles=true` | Lista libros con `stock > 0` | `bibliotecario`, `socio` |
| `CRUD` | `/socios` | Alta, consulta, modificación y baja de socios | `bibliotecario` |
| `POST` | `/prestamos` | Registra un nuevo préstamo | `bibliotecario` |
| `POST` | `/prestamos/{id}/devolucion` | Registra la devolución y calcula multa | `bibliotecario` |
| `GET` | `/socios/{id}/prestamos?activos=true` | Consulta préstamos activos de un socio | `bibliotecario` o el propio `socio` |

## Reglas de Negocio Implementadas

1. **Límite de préstamos:** Un socio no puede tener más de **3 préstamos activos** simultáneos (`409 Conflict`).
2. **Control de stock:** No se puede prestar un libro sin stock (`409 Conflict`). Al prestar, se descuenta `1` del stock.
3. **Estado del socio:** Un socio inactivo (`activo = false`) no puede solicitar préstamos (`403 Forbidden`).
4. **Plazo de préstamo:** El vencimiento se calcula automáticamente a **14 días** de la fecha de préstamo (`fecha_vencimiento = fecha_prestamo + 14 días`).
5. **Devolución y multas:** Al devolver se repone `1` al stock y se calcula la multa a razón de **$\$100$ por día de atraso** ($\$0$ si se devuelve en término).
6. **Doble devolución:** No se permite devolver un préstamo que ya fue devuelto (`409 Conflict`).
7. **Recursos inexistentes:** Cualquier operación sobre un ID inexistente devuelve `404 Not Found`.
8. **Unicidad e integridad:** No se permiten ISBN ni emails duplicados, ni eliminar libros con préstamos asociados (`409 Conflict`).

## Cómo Correr los Tests y Ver la Cobertura

La suite de pruebas utiliza SQLite en memoria (`sqlite://`) y cubre CRUDs, relaciones, reglas de negocio, base de datos y control de roles (objetivo de cobertura $\ge 80\%$):

```
pytest
pytest --cov=. --cov-report=term-missing
```