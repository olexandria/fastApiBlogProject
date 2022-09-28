import json
from fastapi import status
from blog import models


def test_create_blog_without_authentication(client, db_session):
    data = {
        "title": "blog_test",
        "body": "body_test",
    }
    response = client.post("/blog/", data=json.dumps(data))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert db_session.query(models.Blog).count() == 0
    assert response.json() == {"detail": "Not authenticated"}


def test_create_blog_with_authentication(client, normal_user_token_headers, db_session):
    data = {
        "title": "SDE super",
        "body": "doogle",
    }
    response = client.post("/blog/", data=json.dumps(data), headers=normal_user_token_headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert db_session.query(models.Blog).count() == 1
    assert response.json()["title"] == "SDE super"
    assert response.json()["body"]
    assert response.json()["user_id"]


def test_get_all_blogs(client, normal_user_token_headers, db_session):
    data = {
        "title": "blog1",
        "body": "body1",
    }
    data1 = {
        "title": "blog2",
        "body": "body2",
    }
    client.post("/blog/", data=json.dumps(data), headers=normal_user_token_headers)
    client.post("/blog/", data=json.dumps(data1), headers=normal_user_token_headers)
    response = client.get("/blog/", headers=normal_user_token_headers)
    assert db_session.query(models.Blog).count() == 2
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    assert response.json()[1]["body"] == "body2"


def test_get_nonexistent_blog(client, normal_user_token_headers, db_session):
    response = client.get("/blog/1", headers=normal_user_token_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_blog(client, normal_user_token_headers, db_session):
    data = {
        "title": "SDE super",
        "body": "doogle",
    }
    blog = client.post("/blog/", data=json.dumps(data), headers=normal_user_token_headers)
    response = client.delete(f"/blog/{blog.json()['id']}", headers=normal_user_token_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert db_session.query(models.Blog).count() == 0


def test_update_blog(client, normal_user_token_headers, db_session):
    data = {
        "title": "SDE super",
        "body": "doogle",
    }
    blog = client.post("/blog/", data=json.dumps(data), headers=normal_user_token_headers)
    updated_data = {
        "title": "updated title",
        "body": "updated body",
    }
    response = client.put(f"/blog/{blog.json()['id']}", data=json.dumps(updated_data),
                          headers=normal_user_token_headers)
    updated_blog = client.get(f"/blog/{blog.json()['id']}", headers=normal_user_token_headers)
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json() == ["Successfully updated!"]
    assert updated_blog.json()["title"] == "updated title"
    assert updated_blog.json()["body"] == "updated body"
