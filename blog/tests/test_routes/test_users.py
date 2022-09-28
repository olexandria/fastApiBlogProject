import json
from fastapi import status

from blog import models


def test_create_user(client, db_session):
    data = {"name": "testuser", "email": "testuser@nofoobar.com", "password": "testing"}
    response = client.post("/user/", json.dumps(data))
    assert response.status_code == status.HTTP_201_CREATED
    assert db_session.query(models.User).count() == 1
    assert response.json()["email"] == "testuser@nofoobar.com"


def test_get_user(client):
    data = {"name": "testuser111", "email": "testuser@nofoobar.com", "password": "testing"}
    client.post("/user/", json.dumps(data))
    response = client.get("/user/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "testuser111"


def test_get_all_users(client):
    data = {"name": "testuser111", "email": "testuser@nofoobar.com", "password": "testing"}
    data1 = {"name": "testuser222", "email": "testuser222@nofoobar.com", "password": "testing"}
    client.post("/user/", json.dumps(data))
    client.post("/user/", json.dumps(data1))
    response = client.get("/user/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    assert response.json()[1]["email"] == "testuser222@nofoobar.com"
