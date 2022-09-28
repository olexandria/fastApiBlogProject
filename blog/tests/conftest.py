from typing import Any
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from blog import models
from blog.database import get_db
from blog.main import app
from blog.tests.test_routes.utils.users import authentication_token_from_email

SQLALCHEMY_DATABASE_URL = "sqlite:///./blog/tests/test_db.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session() -> Generator[SessionTesting, Any, None]:
    models.Base.metadata.create_all(engine)

    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    models.Base.metadata.drop_all(engine)
    connection.close()


@pytest.fixture(scope="function")
def client(db_session: SessionTesting) -> Generator[TestClient, Any, None]:
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def normal_user_token_headers(client: TestClient, db_session: SessionTesting):
    return authentication_token_from_email(client=client, email="test@example.com", db=db_session)
