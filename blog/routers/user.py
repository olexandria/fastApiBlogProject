from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from blog import schemas, database
from ..repository import user

router = APIRouter(
    prefix="/user",
    tags=['Users']
)


@router.get('/', response_model=List[schemas.ShowUserBlogs])
def get_all_users(db: Session = Depends(database.get_db)):
    return user.get_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    return user.create(request, db)


@router.get('/{id}', status_code=200, response_model=schemas.ShowUserBlogs)
def get_user(id: int, db: Session = Depends(database.get_db)):
    return user.get_one(id, db)
