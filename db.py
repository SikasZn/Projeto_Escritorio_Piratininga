from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# 🔑 Configure sua URL do Render/AWS/Railway aqui
# Exemplo: postgresql+psycopg2://usuario:senha@host:5432/banco
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://piratininga_db_user:IzLVRJ8GWGuUoicPZSvmg08AeQ04JZMt@dpg-d3eqovumcj7s73dnst90-a.oregon-postgres.render.com/piratininga_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Lancamento(Base):
    __tablename__ = "lancamentos"

    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String, nullable=False)
    data = Column(Date, nullable=False)
    descricao = Column(String, nullable=False)
    receita = Column(Float, default=0.0)
    despesa = Column(Float, default=0.0)

def init_db():
    Base.metadata.create_all(bind=engine)