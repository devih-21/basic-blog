from fastapi import Depends, FastAPI, status, Response, HTTPException
import schemas, models
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import uuid
from typing import List
from sqlalchemy.sql import func
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4

origins = [
  "http://localhost",
  "http://localhost:3000",
  "http://localhost:8000"
]




models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
  expose_headers=["*"]
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@app.get('/blog-posts', status_code=status.HTTP_200_OK, response_model=List[schemas.Post], tags=["Blogs"])
def home(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.post('/create-blog-posts', status_code=201, tags=["Blogs"])
def create_blog(request: schemas.Post, db: Session = Depends(get_db)):
    id_blog = uuid4()
    new_blog = models.Blog(id=str(id_blog), title=request.title, body=request.body, created_at=request.created_at, published=request.published)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog/{id}', status_code=200, response_model=schemas.GetPost, tags=["Blogs"],)
def get_blog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} is not available",
        )
    return blog



@app.put('/update/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostUpdate, tags=["Blogs"])
async def update_post_by_id(id, request: schemas.PostUpdate, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    # updated_blog = request.dict()
    # blog.update(updated_blog)
    # db.commit()
    blog.title = request.title
    blog.body = request.body
    blog.published = request.published
    blog.updated_at = func.now()
    
    db.commit()
    return blog

@app.delete('/blog/{id}', status_code=204, tags=["Blogs"])
def delete_blog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with `{id}` not found")
    
    blog.delete(synchronize_session=False)
    db.commit()
    return f'Blog with id {id} is deleted successfully'

