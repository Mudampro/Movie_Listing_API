from sqlalchemy.orm import Session
from app import schema, models




@staticmethod
def create_comment(db: Session, comment: schema.CommentCreate, user_id: int, movie_id: int):
    db_comment = models.Comment(
        comment_text=comment.comment_text,
        movie_id=movie_id,
        user_id=user_id,
        parent_id=comment.parent_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


@staticmethod
def get_comment(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()


@staticmethod
def get_comments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Comment).offset(skip).limit(limit).all()


@staticmethod
def update_comment(db: Session, comment_id: int, comment: schema.CommentUpdate):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if db_comment:
        for key, value in comment.dict().items():
            setattr(db_comment, key, value)
        db.commit()
        db.refresh(db_comment)
    return db_comment


@staticmethod
def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if db_comment:
        db.delete(db_comment)
        db.commit()
    return db_comment
