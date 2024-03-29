
from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from sqlalchemy import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

class Post(Base) : 
     __tablename__ = "posts"
     
     id = Column(Integer, primary_key=True, nullable=False)
     title = Column(String, nullable=False)
     content = Column(String, nullable=False)
     published = Column(Boolean, server_default='TRUE', nullable=True)
     created_at = Column(TIMESTAMP(timezone = true), nullable=False, server_default=text('now()'))
     #Fetch on the user based on the owner id and returned it as proprety
     owner = relationship("User")

class User(Base):
    __tablename__ = "users"
     
     id = Column(Integer, primary_key=True, nullable=False)
     email: Column(String, nullable=False, unique: True)
     password: Column(String, nullable=False)
     created_at = Column(TIMESTAMP(timezone = true), nullable=False, server_default=text('now()'))

class Vote(Base):
   __tablename__="votes"
   user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
   post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)

