from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from blog import schemas, database
from blog.repository import blog
from blog import oauth2

router = APIRouter(
    prefix="/blog",
    tags=['Blogs']
)


@router.get('/', response_model=List[schemas.ShowBlog])
def get_all_blogs(db: Session = Depends(database.get_db),
                  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.get_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(database.get_db),
                current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.create(request, db)


@router.post('/{id}', status_code=status.HTTP_201_CREATED)
def add_comment(id, request: schemas.CommentBase, db: Session = Depends(database.get_db),
                current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.add_comment(id, request, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id, db: Session = Depends(database.get_db),
                current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.delete(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request: schemas.Blog, db: Session = Depends(database.get_db),
                current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.update(id, request, db)


@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def get_blog(id, db: Session = Depends(database.get_db),
             current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.get_one(id, db)
