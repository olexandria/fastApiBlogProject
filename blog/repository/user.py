from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from blog import models, schemas
from blog.hashing import Hash


def create(request: schemas.User, db: Session):
    new_user = models.User(name=request.name, email=request.email,
                           password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all(db: Session):
    users = db.query(models.User).all()
    return users


def get_one(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The user doesn't exist yet!")
    return user


def get_user_by_email(email: str, db: Session):
    user = db.query(models.User).filter(models.User.email == email).first()
    return user
