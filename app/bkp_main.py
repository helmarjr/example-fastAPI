import psycopg2
import time
from sqlalchemy.orm import Session
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Response, status, HTTPException, Depends
from . import models, schemas
from .database import engine, get_db

# Models
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Database
# while True:
#     try:
#         conn = psycopg2.connect(
#                                 host='localhost', 
#                                 database='fastapi', 
#                                 user='postgres', 
#                                 password='Bundamole22',
#                                 cursor_factory=RealDictCursor
#                                 )
#         cursor = conn.cursor()
#         print("Database connection was succesfull!")
#         break
#     except Exception as e:
#         print(f"Connection database is failed: {e}")
#         time.sleep(2)


# CREATE 
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute('''INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *''', 
    #                 (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # este modo fica muito dificil de declarar quando temos muitos campos
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)

    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {'data': new_post}


# SELECT
@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):  
    # cursor.execute('SELECT * FROM posts ORDER BY created_at')
    # posts = cursor.fetchall()

    posts = db.query(models.Post).order_by(models.Post.id).all()

    return {'data': posts}

 
@app.get('/posts/{id}')
def get_posts_id(id: int, db: Session = Depends(get_db)):
    
    # cursor.execute(''' SELECT * FROM posts WHERE id = %s ''', (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id: {id} not found')

    return {'post_detail': post}


# UPDATE
@app.put('/posts/{id}')
def update_posts_id(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute('''UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *''', 
    #                 (post.title, post.content, post.published, id))
    # up_post = cursor.fetchone()
    # conn.commit()
    
    up_post = db.query(models.Post).filter(models.Post.id == id)

    if not up_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id: {id} not found')

    up_post.update(post.dict())
    db.commit()

    return {'data': up_post.first()}


# DELETE
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_posts_id(id: int, db: Session = Depends(get_db)):
    
    # cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING *''', (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    deleted_post = db.query(models.Post).filter(models.Post.id == id)


    if not deleted_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} not found')

    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# uvicorn main:app --reload
# uvicorn app.main:app --reload
# http://127.0.0.1:8000/redoc
# http://127.0.0.1:8000/docs