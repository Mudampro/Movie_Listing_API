from sqlalchemy.orm import Session
from app import schema, models




@staticmethod
def create_rating(db: Session, rating: schema.RatingCreate, user_id: int, movie_id: int):
    db_rating = models.Rating(**rating.dict(), user_id=user_id, movie_id=movie_id)
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating


@staticmethod
def get_movie_by_id(db: Session, movie_id: int):
    return db.query(models.Movie).filter_by(id=movie_id).first()


@staticmethod
def get_ratings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Rating).offset(skip).limit(limit).all()


@staticmethod
def get_rating(db: Session, rating_id: int):
    return db.query(models.Rating).filter(models.Rating.id == rating_id).first()

@staticmethod
def update_rating(db: Session, rating_id: int, rating: schema.RatingUpdate):
    db_rating = db.query(models.Rating).filter(models.Rating.id == rating_id).first()
    if db_rating:
        for key, value in rating.dict().items():
            setattr(db_rating, key, value)
        db.commit()
        db.refresh(db_rating)
    return db_rating


@staticmethod
def delete_rating(db: Session, rating_id: int):
    db_rating = db.query(models.Rating).filter(models.Rating.id == rating_id).first()
    if not db_rating:
        return None
    db.delete(db_rating)
    db.commit()
    return db_rating