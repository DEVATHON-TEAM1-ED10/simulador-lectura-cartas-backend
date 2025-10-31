from sqlalchemy import Column, Integer, String
from app.db.session import Base


class Card(Base):
    __tablename__ = "Card"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    meaning = Column(String, nullable=False)
    image = Column(String, nullable=False)
    energy = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f"<Card(id={self.id}, name={self.name}, meaning={self.meaning}, image={self.image}, energy={self.energy}>"
