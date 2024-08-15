from fastapi import Depends, HTTPException, APIRouter, status
from app import schema
from sqlalchemy.orm import Session
from app.db import get_db
from app.crud import user_crud
from app.logger import get_logger



logger = get_logger(__name__)

user_router = APIRouter()

@user_router.post("/user/",status_code=status.HTTP_201_CREATED, response_model=schema.User)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_username(db, username=user.username)
    if db_user:
        logger.warning(f"User with {user.username} already exists.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    logger.info("User successfully created.")
    return user_crud.create_user(db=db, user=user)

@user_router.get("/users/",status_code=status.HTTP_200_OK, response_model=list[schema.User])
def get_users(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    users = user_crud.get_users(db, skip=skip, limit=limit)
    logger.info(f"Details of users within the range retrieved successfully")
    return users

@user_router.get("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=schema.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user(db, user_id)
    if not user:
        logger.warning(f"User with username passed not found")
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.put("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=schema.User)
def update_user(user_id: int, user: schema.UserUpdate, db: Session = Depends(get_db)):
    db_user = user_crud.update_user(db, user_id, user)
    if not db_user:
        logger.warning(f"User with {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@user_router.delete("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=schema.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.delete_user(db, user_id)
    if not db_user:
        logger.warning(f"User with {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

