from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

# Base declarativa
Base = declarative_base()

# URL
DATABASE_URL = "sqlite:///./dev.db"

# Crear motor
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependencia
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
