from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from .user import get_user_by_email
from .. import models, schemas


def create(request: schemas.Blog, db: Session):
    # creator_id = get_user_by_email(user.email, db).id
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def delete(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The blog with the id {id} doesn't exist!")

    blog.delete(synchronize_session=False)
    db.commit()
    return {'Successfully deleted!'}


def update(id: int, request: schemas.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The blog with the id {id} doesn't exist!")

    blog.update(request.__dict__, synchronize_session=False)
    db.commit()
    return {'Successfully updated!'}


def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def get_one(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The blog with the id {id} doesn't exist!")
    return blog


def add_comment(id: int, request: schemas.CommentBase, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The blog with the id {id} doesn't exist!")

    comment = models.Comment(comment=request.comment, created_at=datetime.now(),
                             user_id=1, blog_id=id)
    db.add(comment)
    db.commit()
    db.refresh(comment)

    return {'Comment added successfully!'}
