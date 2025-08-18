import datetime
import os
import atexit
from sqlalchemy import create_engine, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, MappedColumn

POSTGRES_USER = os.getenv('POSTGRES_USER', "postgres")
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', "1234")
POSTGRES_HOST = os.getenv('POSTGRES_HOST', "127.0.0.1")
POSTGRES_PORT = os.getenv('POSTGRES_PORT', "5432")
POSTGRES_DB = os.getenv('POSTGRES_DB', "flask_db")

PG_DSN = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

engine = create_engine(PG_DSN)

Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):

    @property
    def id_dict(self):
        return {"id": self.id}


class Advertisement(Base):
    __tablename__ = "advertisements"

    id: MappedColumn[int] = mapped_column(Integer, primary_key=True)
    title: MappedColumn[str] = mapped_column(String)
    description: MappedColumn[str] = mapped_column(String)
    owner: MappedColumn[str] = mapped_column(String)
    create_date: MappedColumn[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "create_date": self.create_date.isoformat(),
            "owner": self.owner,
            "description": self.description,
        }


Base.metadata.create_all(engine)
atexit.register(engine.dispose)
