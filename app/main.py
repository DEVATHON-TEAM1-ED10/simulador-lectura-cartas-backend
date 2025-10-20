from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import cards, predictions

app = FastAPI(title="Tarot API (Docker Dev)")

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
