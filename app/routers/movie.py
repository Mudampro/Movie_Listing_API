from fastapi import APIRouter, Depends, HTTPException, status
from app import schema, security, models
from app.crud import movie_crud
from sqlalchemy.orm import Session
from app.logger import get_logger



logger = get_logger(__name__)



movie_router = APIRouter()



@movie_router.post("/movies/", status_code=status.HTTP_201_CREATED, response_model=schema.Movie)
def create_movie(movie: schema.MovieCreate, db: Session = Depends(security.get_db), current_user: models.User = Depends(security.get_current_user)):
    logger.info("Movie creation initiated successfully.")
    return movie_crud.create_movie(db=db, movie=movie, user_id=current_user.id)


@movie_router.get("/movies/", status_code=status.HTTP_200_OK, response_model=list[schema.Movie])
def get_movies(skip: int = 0, limit: int = 50, db: Session = Depends(security.get_db)):
    movies = movie_crud.get_movies(db, skip=skip, limit=limit)
    logger.info("Movies retrieved successfully.")
    return movies


@movie_router.get("/movie/{movie_id}", status_code=status.HTTP_200_OK, response_model=schema.Movie)
def get_movie(movie_id: int, db: Session = Depends(security.get_db)):
    movie = movie_crud.get_movie(db, movie_id)
    if not movie:
        logger.warning(f"Movie with ID {movie_id} not found.")
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@movie_router.put("/movies/{movie_id}", status_code=status.HTTP_200_OK, response_model=schema.Movie)
def update_movie(movie_id: int, movie: schema.MovieUpdate, db: Session = Depends(security.get_db), current_user: models.User = Depends(security.get_current_user)):
    db_movie = movie_crud.get_movie(db, movie_id)
    if not db_movie or db_movie.user_id != current_user.id:
        logger.warning(f"Movie with ID {movie_id} not found or not authorized.")
        raise HTTPException(status_code=404, detail="Movie not found or not authorized")
    logger.info(f"Movie with ID {movie_id} updated successfully.")
    return movie_crud.update_movie(db=db, movie_id=movie_id, movie=movie)


@movie_router.delete("/movies/{movie_id}", status_code=status.HTTP_200_OK, response_model=schema.Movie)
def delete_movie(movie_id: int, db: Session = Depends(security.get_db), current_user: models.User = Depends(security.get_current_user)):
    db_movie = movie_crud.get_movie(db, movie_id)
    if not db_movie or db_movie.user_id != current_user.id:
        logger.warning(f"Movie with ID {movie_id} not found or not authorized.")
        raise HTTPException(status_code=404, detail="Movie not found or not authorized")
    logger.info(f"Movie with ID {movie_id} deleted successfully.")
    return movie_crud.delete_movie(db=db, movie_id=movie_id)