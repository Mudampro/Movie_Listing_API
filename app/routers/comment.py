from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schema, security, models
from app.crud import comment_crud
from app.db import get_db
from app.logger import get_logger



logger = get_logger(__name__)


comment_router = APIRouter()


@comment_router.post("/movies/{movie_id}/comments/", response_model=schema.Comment)
def create_comment(movie_id: int, comment: schema.CommentCreate, db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    existing_comment = db.query(models.Comment).filter_by(user_id=current_user.id, movie_id=movie_id).first()
    if existing_comment:
        logger.warning(f"User {current_user.id} attempted to comment on the movie with ID {movie_id} more than once.")
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="User has already Commented this movie"
        )
    logger.info(f"User {current_user.id} successfully commented on the movie with ID {movie_id}.")
    return comment_crud.create_comment(db=db, comment=comment, user_id=current_user.id, movie_id=movie_id)



@comment_router.post("/comments/{comment_id}/replies/", response_model=schema.Comment)
def create_reply(comment_id: int, comment: schema.CommentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
    parent_comment = comment_crud.get_comment(db, comment_id)
    if not parent_comment:
        logger.warning(f"Parent comment with ID {comment_id} not found.")
        raise HTTPException(status_code=404, detail="Parent comment not found")
    logger.info(f"User {current_user.id} successfully replied to comment ID {comment_id}.")
    return comment_crud.create_comment(db=db, comment=comment, user_id=current_user.id, movie_id=parent_comment.movie_id)


@comment_router.get("/comments/", response_model=list[schema.Comment])
def get_comments(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    comments = comment_crud.get_comments(db, skip=skip, limit=limit)
    logger.info("Comments retrieved successfully.")
    return comments


@comment_router.get("/comments/{comment_id}", response_model=schema.Comment)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = comment_crud.get_comment(db, comment_id)
    if not comment:
        logger.warning(f"Comment with ID {comment_id} not found.")
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@comment_router.put("/comments/{comment_id}", response_model=schema.Comment)
def update_comment(comment_id: int, comment: schema.CommentUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
    db_comment = comment_crud.get_comment(db, comment_id)
    if not db_comment or db_comment.user_id != current_user.id:
        logger.warning(f"Comment with ID {comment_id} not found or not authorized.")
        raise HTTPException(status_code=404, detail="Comment not found or not authorized")
    logger.info(f"Comment with ID {comment_id} updated successfully.")
    return comment_crud.update_comment(db=db, comment_id=comment_id, comment=comment)


@comment_router.delete("/comments/{comment_id}", response_model=schema.Comment)
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(security.get_current_user)):
    db_comment = comment_crud.get_comment(db, comment_id)
    if not db_comment or db_comment.user_id != current_user.id:
        logger.warning(f"Comment with ID {comment_id} not found or not authorized.")
        raise HTTPException(status_code=404, detail="Comment not found or not authorized")
    logger.info(f"Comment with ID {comment_id} deleted successfully.")
    return comment_crud.delete_comment(db=db, comment_id=comment_id)

