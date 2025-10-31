from .session import Base, engine, SessionLocal
from app.models.card import Card
import json
import os


def seed_cards():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "cards.json")

    with open(json_path, "r", encoding="utf-8") as f:
        cards = json.load(f)

    for card_data in cards:
        if not db.query(Card).filter_by(id=card_data["id"]).first():
            db.add(Card(**card_data))

    db.commit()
    db.close()
    print("✅ Seed completado: cartas insertadas.")


def get_all_cards_in_db():
    db = SessionLocal()

    results = db.query(Card).count()
    print("Las cartas son: ", results)

if __name__ == "__main__":
    seed_cards()
