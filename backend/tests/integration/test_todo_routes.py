from httpx import AsyncClient


async def test_create_todo(client: AsyncClient) -> None:
    res = await client.post("/todos", json={"title": "Buy milk", "description": "Whole"})
    assert res.status_code == 201
    body = res.json()
    assert body["title"] == "Buy milk"
    assert body["description"] == "Whole"
    assert body["completed"] is False
    assert "id" in body


async def test_list_todos(client: AsyncClient) -> None:
    await client.post("/todos", json={"title": "First"})
    await client.post("/todos", json={"title": "Second"})

    res = await client.get("/todos")
    assert res.status_code == 200
    assert len(res.json()) == 2


async def test_update_todo(client: AsyncClient) -> None:
    created = (await client.post("/todos", json={"title": "Original"})).json()

    res = await client.put(f"/todos/{created['id']}", json={"title": "Updated"})
    assert res.status_code == 200
    assert res.json()["title"] == "Updated"


async def test_complete_todo(client: AsyncClient) -> None:
    created = (await client.post("/todos", json={"title": "Do it"})).json()

    res = await client.patch(f"/todos/{created['id']}/complete")
    assert res.status_code == 200
    assert res.json()["completed"] is True


async def test_delete_todo(client: AsyncClient) -> None:
    created = (await client.post("/todos", json={"title": "Remove me"})).json()

    res = await client.delete(f"/todos/{created['id']}")
    assert res.status_code == 204

    res = await client.get("/todos")
    assert len(res.json()) == 0


async def test_update_not_found(client: AsyncClient) -> None:
    res = await client.put("/todos/00000000-0000-0000-0000-000000000000", json={"title": "X"})
    assert res.status_code == 404


async def test_complete_not_found(client: AsyncClient) -> None:
    res = await client.patch("/todos/00000000-0000-0000-0000-000000000000/complete")
    assert res.status_code == 404


async def test_delete_not_found(client: AsyncClient) -> None:
    res = await client.delete("/todos/00000000-0000-0000-0000-000000000000")
    assert res.status_code == 404
