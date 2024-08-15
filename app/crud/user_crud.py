from sqlalchemy.orm import Session
from app import schema, models
from passlib.context import CryptContext
from app.security import get_password_hash


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



@staticmethod
def create_user(db: Session, user: schema.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        full_name=user.full_name,
        phone_number=user.phone_number,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@staticmethod
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


@staticmethod
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


@staticmethod
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


@staticmethod
def create_user(db: Session, user: schema.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username, 
        full_name=user.full_name,
        phone_number=user.phone_number,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@staticmethod
def update_user(db: Session, user_id: int, user: schema.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    db_user.full_name = user.full_name
    db_user.phone_number = user.phone_number
    db.commit()
    db.refresh(db_user)
    return db_user


@staticmethod
def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user