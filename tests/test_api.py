import pytest
from httpx import AsyncClient, ASGITransport
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from api.main import app


@pytest.mark.asyncio
async def test_get_books():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        ) as ac:
        response = await ac.get("/get-books")
        assert response.status_code == 200
        data = response.json()

        assert len(data) >= 50


@pytest.mark.asyncio
async def test_create_book():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        response = await ac.post("/create-book", json={
            "title": "Test Book(pytest)",
            "author": "Автор авторов",
        })
        assert response.status_code == 200

        data = response.json()
        assert data == {"message": "Книга создана"}
