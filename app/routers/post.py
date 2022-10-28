from .. import models, schemas, oauth2
from app import oauth2
from typing import List, Optional
from fastapi import HTTPException, APIRouter, Response, Depends, status
from ..database import get_db
from sqlalchemy import func
from sqlalchemy.orm import Session


router = APIRouter(
    prefix='/posts', 
    tags=['Posts']
)

# ================== CREATE ==================
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id = current_user.id,  **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    print(current_user)

    return new_post


# ================== SELECT ==================
@router.get('/')
# @router.get('/', response_model=List[schemas.Post])
def get_posts(  db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user),
                limit: int = 5,
                skip: int = 0,
                search: Optional[str] = ''
                ):  

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).order_by(models.Post.id).limit(limit).offset(skip).all()

    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label('votes'))
          .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)  # outer = left join
          .filter(models.Post.title.contains(search))
          .group_by(models.Post.id)
          .order_by(models.Post.id)
          .limit(limit)
          .offset(skip)
          .all()
    ) 

    return results

 
@router.get('/{id}', response_model=schemas.PostOut)
# @router.get('/{id}', response_model=schemas.PostOut)
def get_posts_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = (
        db.query(models.Post, func.count(models.Vote.post_id).label('votes'))
          .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
          .filter(models.Post.id == id)
          .group_by(models.Post.id)
          .order_by(models.Post.id)
          .first()
    )

    # post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id: {id} not found')
    
    if post_query.Post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'not authorized to perform requested action')

    
    return post_query



# ================== UPDATE ==================
@router.put('/{id}', response_model=schemas.Post)
def update_posts_id(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    up_post = post_query.first()

    if not up_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id: {id} not found')

    if up_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'not authorized to perform requested action')


    post_query.update(post.dict())
    db.commit()

    return up_post


# ================== DELETE ==================
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_posts_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} not found')
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'not authorized to perform requested action')

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


