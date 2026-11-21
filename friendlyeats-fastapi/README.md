# FriendlyEats FastAPI — Sprint 1

   Autor: Luciano Raziel Martinez Mendoza · Matrícula: Utp0201986 · Materia: Optativa · Grupo: B

CRUD de restaurantes con FastAPI, Firestore (emulador local) y vistas HTML con Jinja2.
Alcance del Sprint 1: sin autenticación, reseñas, imágenes ni despliegue.

## Requisitos
Python 3.11+, Node.js, Java (JDK 11+), Git y Firebase CLI (`npm install -g firebase-tools`).

## Puesta en marcha
```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env               # Windows: copy .env.example .env  -> edita FIREBASE_PROJECT_ID
firebase login
firebase use <tu-proyecto-id>
```

## Comandos
```bash
# Terminal 1: emulador Firestore (UI en http://localhost:4000)
firebase emulators:start --only firestore

# Terminal 2: aplicación (http://localhost:8000, docs en /docs)
uvicorn app.main:app --reload

# Datos iniciales (10 restaurantes)
python -m scripts.seed

# Pruebas (requieren el emulador encendido)
pytest -v
```

## Arquitectura
`api/v1/restaurants.py` (rutas) → `services/restaurant_service.py` (reglas, 404/400) →
`repositories/restaurant_repository.py` (único acceso a Firestore) → colección `restaurants`.
Validación en `domain/schemas.py` (Pydantic). Vistas en `app/templates`, estáticos en `static/`.

## Endpoints
- `GET /health`
- `POST /api/v1/restaurants` · `GET /api/v1/restaurants?city=&category=&price=&order_by=name|avgRating&limit=20&start_after=<id>`
- `GET|PATCH|DELETE /api/v1/restaurants/{id}`
- Vistas: `/`, `/restaurants/new`, `/restaurants/{id}`, `/restaurants/{id}/edit`

## Decisiones
- ID autogenerado por Firestore; `avgRating` y `numRatings` inician en 0.
- PATCH actualiza solo los campos enviados y permitidos.
- Filtros combinados con orden pueden requerir índices compuestos al desplegar a producción (el emulador no los exige).
- `.gitignore` excluye `*.json` salvo `package.json` y `firebase.json`; nunca subas la cuenta de servicio.
