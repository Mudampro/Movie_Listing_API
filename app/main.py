from fastapi import FastAPI
from app import models
from app.db import engine
from app.routers.user import user_router
from app.routers.movie import movie_router
from app.routers.rating import rating_router
from app.routers.login import login_router
from app.routers.comment import comment_router


import os
import uvicorn



models.Base.metadata.create_all(bind=engine)


app = FastAPI()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)



app.include_router(login_router)
app.include_router(user_router, prefix="/Users", tags=["Users"])
app.include_router(movie_router, prefix="/Movies", tags=["Movies"])
app.include_router(rating_router, prefix="/Ratings", tags=["Ratings"])
app.include_router(comment_router, prefix="/Comments", tags=["Comments"])


@app.get("/")
def Home():
    return {"Success":
            "Welcome to My Third Semester Capstone Project @ AltSchool Africa"}