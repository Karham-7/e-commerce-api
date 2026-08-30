import pytest


@pytest.mark.asyncio
async def test_get_categories(client):
    response = await client.get(
        "/api/v1/categories/"
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_category(admin_client):
    response = await admin_client.post(
        "/api/v1/categories/",
        json={
            "name": "Electronics"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Electronics"


@pytest.mark.asyncio
async def test_update_category(admin_client):
    create_response = await admin_client.post(
        "/api/v1/categories/",
        json={
            "name": "Electronics"
        }
    )

    category_id = create_response.json()["id"]

    response = await admin_client.patch(
        f"/api/v1/categories/{category_id}",
        json={
            "name": "Computers"
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Computers"


@pytest.mark.asyncio
async def test_delete_category(admin_client):
    create_response = await admin_client.post(
        "/api/v1/categories/",
        json={
            "name": "Electronics"
        }
    )

    category_id = create_response.json()["id"]

    response = await admin_client.delete(
        f"/api/v1/categories/{category_id}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == category_id


@pytest.mark.asyncio
async def test_get_category_not_found(client):
    response = await client.get(
        "/api/v1/categories/999999"
    )

    assert response.status_code == 404