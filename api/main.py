import sys
from pathlib import Path
from typing import Annotated

sys.path.append(str(Path(__file__).parent.parent))


from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from config import settings as cfg
from sqlalchemy import Select, Delete


engine = create_async_engine(f"postgresql+asyncpg://{cfg.DB_USER}:{cfg.DB_PASS}@{cfg.DB_HOST}:{cfg.DB_PORT}/{cfg.DB_NAME}")

new_session = async_sessionmaker(engine, expire_on_commit=False)
app = FastAPI()

async def get_session():
    async with new_session() as session:
        yield session
        

SessionDep = Annotated[AsyncSession, Depends(get_session)]
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str]
    
class Books(Base):
    __tablename__ = "books"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]


class BooksSchema(BaseModel):
    id: int
    title: str
    author: str


class BooksCreateSchema(BaseModel):
    title: str
    author: str

class BooksDeleteSchema(BaseModel):
    id: int



@app.get("/setup-database")
async def setup_database():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        
    return {"message": "Database setup complete."}

@app.get("/get-user")
async def get_user():
    pass


@app.post("/create-book")
async def create_book(book: BooksCreateSchema, session: SessionDep):
    try:
        book_obj = Books(title=book.title, author=book.author)
        session.add(book_obj)
        await session.commit()
        await session.refresh(book_obj)
        return {"message": "Книга создана"}
    except Exception as e:
        try:
            await session.rollback()
        except:
            pass
        return {"message": f"Ошибка при создании книги: {e}"}, 400

@app.get("/get-books")
async def get_books(session: SessionDep):
    try:
        query = Select(Books)
        stp = await session.execute(query)
        result = stp.scalars().all()
        return result
    except Exception as e:
        return {"message": f"Ошибка при получении книг: {e}"}, 400




@app.delete("/delete-book")
async def delete_book(id: int, session: SessionDep):
    query = Select(Books).where(Books.id == id)
    result = await session.execute(query)
    book = result.scalars().first()
    if not book:
        return {"message": "Книга не найдена"}
    await session.delete(book)
    await session.commit()
    return {"message": "Книга удалена"}

