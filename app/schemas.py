from pydantic import BaseModel, EmailStr
from datetime import datetime
from tying import Optional
from pydantic.types import conint

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
        id: int
        email: EmailStr
        created_at: datetime
        class config:
            orm_mode: True

class Post(BaseModel):
    title: str
    content: str
    published: bool
    created_at: datetime
    owner_id: int
    owner: UserOut

    class config:
        orm_mode: True

class UserCreate(BaseModel):
        email: EmailStr
        password: str

class UserLogin(BaseModel):
        email: EmailStr
        password: str

class Token(BaseModel):
        access_token: str
        token_type: str

class TokenData(BaseModel):
        id: Optional[String] = None

class Vote(BaseModel):
        post_id: int
        dir: conint(le=1) #le=1 means less or equal 1



