from blog.repository.user import create
from blog.repository.user import get_user_by_email
from fastapi.testclient import TestClient
from blog.schemas import User
from sqlalchemy.orm import Session


def user_authentication_headers(client: TestClient, email: str, password: str):
    data = {"username": email, "password": password}
    r = client.post("/login/", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def authentication_token_from_email(client: TestClient, email: str, db: Session):
    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """
    password = "random-passW0rd"
    user = get_user_by_email(email=email, db=db)
    if not user:
        user_in_create = User(name=email, email=email, password=password)
        user = create(request=user_in_create, db=db)
    return user_authentication_headers(client=client, email=email, password=password)
