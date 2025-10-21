import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))


from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from fastapi import FastAPI

from config import settings as cfg


engine = create_async_engine(f"postgresql+asyncpg://{cfg.DB_USER}:{cfg.DB_PASS}@{cfg.DB_HOST}:{cfg.DB_PORT}/{cfg.DB_NAME}")

new_session = async_sessionmaker(engine, expire_on_commit=False)
app = FastAPI()

async def get_session():
    async with new_session() as session:
        yield session
        
        
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str]
    


@app.get("/setup-database")
async def setup_database():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        
    return {"message": "Database setup complete."}

@app.get("/get-user")
async def get_user():
    pass
    
    