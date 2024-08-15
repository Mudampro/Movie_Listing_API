from pydantic import BaseModel, ConfigDict
from typing import Optional

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    full_name: str
    phone_number: str
    password: str

class UserUpdate(BaseModel):
    full_name: str
    phone_number: str

class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes = True)

        
class Token(BaseModel):
    access_token: str
    token_type: str


class MovieBase(BaseModel):
    title: str
    director: str
    genre: str
    release_year: int

class MovieCreate(MovieBase):
    pass

class MovieUpdate(MovieBase):
    pass

class Movie(MovieBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes = True)


class RatingBase(BaseModel):
    rating: float

class RatingCreate(RatingBase):
    pass

class RatingUpdate(RatingBase):
    pass

class Rating(RatingBase):
    id: int
    user_id: int
    movie_id: int

    model_config = ConfigDict(from_attributes = True)



class CommentBase(BaseModel):
    comment_text: str
    parent_id: Optional[int] = None


class CommentCreate(CommentBase):
    pass


class CommentUpdate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    movie_id: int
    user_id: int
    

    model_config = ConfigDict(from_attributes = True)