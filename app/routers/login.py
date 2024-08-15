from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session
from app import schema, security
from app.crud import user_crud
from app.db import get_db
from app.logger import get_logger


logger = get_logger(__name__)


login_router = APIRouter(
    tags=["Authentication"]
)


@login_router.post("/login",status_code=status.HTTP_200_OK, response_model=schema.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logger.info("Generating authentication token...")
    user = user_crud.get_user_by_username(db, form_data.username)
    if not user:
        logger.warning("Failed login attempt: Incorrect username.")
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not security.verify_password(form_data.password, user.hashed_password):
        logger.warning(f"Failed login attempt for user {form_data.username}: Incorrect password.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    logger.info(f"Token generated for {user.username}")
    return {"access_token": access_token, "token_type": "bearer"}
