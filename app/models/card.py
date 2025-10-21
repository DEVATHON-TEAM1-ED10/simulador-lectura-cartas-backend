from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Card(Base):
    __tablename__ = "Card"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    meaning = Column(String, nullable=False)
    image = Column(String, nullable=False)
    energy = Column(Integer, nullable=False)
