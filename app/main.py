from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
# ✅ importa directamente los routers, no el paquete
from app.api.routes.cards import router as cards_router
from app.api.routes.predictions import router as predictions_router  # si ya existe
from app.db.seed import get_all_cards_in_db, seed_cards

@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_cards()
    get_all_cards_in_db()
    yield


app = FastAPI(title="Tarot API (Docker Dev)", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/health")
def health():
    return {"status": "ok", "message": "running in docker"}


# 👇 Importante: enganchar rutas stub
app.include_router(cards_router)
app.include_router(predictions_router)
