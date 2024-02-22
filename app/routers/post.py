from typing  import Optional, List 
from fastapi import FastAPI, Response, Status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth
from ..database import get_db
from sqlalchemy import func 

router = APIRouter(
    prefix = "/posts",
    tags = "Posts"
)

@router.get("/", response_model: List[schemas.Post]) ###@router.get("/", response_model: List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user = int = Depends(oauth.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str]=""):
    #print(limit)
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() 

    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() #filter(models.Post.owner_id == current_user.id) is to retrieve all the posts of the logged-in user. BUT IF I WANT MY POSTS ARE PUBLIC I CAN JUST REMOVE THIS FILTER METHOD.

    ###results = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).join(models.Vote, models.Vote.post_is == models.Post.id, isouter=True).group_by(models.Post.id).all()
    ###return results
    return posts

@router.get("/{id}", response_model: schemas.Post)
def get_posts(id: int, db: Session = Depends(get_db), current_user = int = Depends(oauth.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found)
    #check if the id of the post owner is the same id of the user logged in. BUT IF I WANT MY POSTS ARE PUBLIC I CAN JUST REMOVE THIS EXCEPTION.
    if post.owner_id != current_user.id:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform that action.)
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model: schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user = int = Depends(oauth.get_current_user)):
    print(current_user)#print(current_user.email)
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(owner_id=current_user.id, **post.dict())#if there is too much columns use **post.dict()
                                                                   #owner_id for returning user_id forign key column automatically
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_model: schemas.Post)
def delete_posts(id: int, db: Session = Depends(get_db), current_user = int = Depends(oauth.get_current_user)):
    #send a query
    post_query = db.query(models.Post).filter(models.Post.id == id)
    #find the post
    post = post_query.first()
    #if there is no post found
    if post.first() == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist.)
    #check if the id of the post owner is the same id of the user logged in.
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform that action.)
    #if post found delete it
    post.delete(synchronize_session=False)
    db.commit()
    return post

@app.put("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_model: schemas.Post)
def update_posts(id: int, updated_post= schemas.PostCreate, db: Session = Depends(get_db),current_user = int = Depends(oauth.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist.)
    #check if the id of the post owner is the same id of the user logged in
    if post.owner_id != current_user.id:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform that action.)
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


