from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import cards, predictions
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


@app.get("/health")
def health():
    return {"status": "ok", "message": "running in docker"}


# 👇 Importante: enganchar rutas stub
app.include_router(cards.router)
app.include_router(predictions.router)
