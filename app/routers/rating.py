from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from app import schema, security, models
from app.crud import rating_crud
from sqlalchemy.orm import Session
from app.db import get_db
from app.logger import get_logger



logger = get_logger(__name__)


rating_router = APIRouter()



@rating_router.post("/movies/{movie_id}/ratings/", response_model=schema.Rating)
def create_rating(movie_id: int, rating: schema.RatingCreate, db: Session = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
    movie = rating_crud.get_movie_by_id(db, movie_id)
    if not movie:
        logger.warning(f"Movie with ID {movie_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Movie Id or Movie not found"
        )    
    if rating.rating < 1 or rating.rating > 10:
        logger.warning("Invalid rating value provided.")
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail = "Ratings of a movie must not be less than 1 and greater than 10"
        )
    existing_rating = db.query(models.Rating).filter_by(user_id=current_user.id, movie_id=movie_id).first()
    if existing_rating:
        logger.warning(f"User {current_user.id} attempted to rate the movie with ID {movie_id} more than once.")
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="User has already rated this movie"
        )
    logger.info(f"User {current_user.id} successfully rated the movie with ID {movie_id}.")
    return rating_crud.create_rating(db=db, rating=rating, user_id=current_user.id, movie_id=movie_id)


@rating_router.get("/ratings/", response_model=list[schema.Rating])
def get_ratings(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    ratings = rating_crud.get_ratings(db, skip=skip, limit=limit)
    logger.info("Ratings retrieved successfully.")
    return ratings

@rating_router.get("/ratings/{rating_id}", response_model=schema.Rating)
def get_rating(rating_id: int, db: Session = Depends(get_db)):
    rating = rating_crud.get_rating(db, rating_id)
    if not rating:
        logger.warning(f"Rating with ID {rating_id} not found.")
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating

@rating_router.put("/ratings/{rating_id}", response_model=schema.Rating)
def update_rating(rating_id: int, rating: schema.RatingUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
    db_rating = rating_crud.get_rating(db, rating_id)
    if not db_rating or db_rating.user_id != current_user.id:
        logger.warning(f"Rating with ID {rating_id} not found or not authorized.")
        raise HTTPException(status_code=404, detail="Rating not found or not authorized")
    if rating.rating < 1 or rating.rating > 10:
        logger.warning("Invalid rating value provided.")
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail = "Ratings of a movie must not be less than 1 and greater than 10"
        )
    logger.info(f"Rating with ID {rating_id} updated successfully.")
    return rating_crud.update_rating(db=db, rating_id=rating_id, rating=rating)

@rating_router.delete("/ratings/{rating_id}", response_model=schema.Rating)
def delete_rating(rating_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
    db_rating = rating_crud.get_rating(db, rating_id)
    if not db_rating or db_rating.user_id != current_user.id:
        logger.warning(f"Rating with ID {rating_id} not found or not authorized.")
        raise HTTPException(status_code=404, detail="Rating not found or not authorized")
    logger.info(f"Rating with ID {rating_id} deleted successfully.")
    return rating_crud.delete_rating(db=db, rating_id=rating_id)