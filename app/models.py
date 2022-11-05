import sqlalchemy.orm
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
from app import database
from datetime import datetime


class Post(database.Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default=text("true"))
    created_at = Column('timestamp',
                        TIMESTAMP(timezone=False),
                        nullable=False,
                        server_default=text("NOW()"),
                        )
    owner_id = Column(Integer,
                      ForeignKey("users.id", ondelete="CASCADE"),
                      nullable=False)
    owner = sqlalchemy.orm.relationship("User") # class User

class User(database.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column('timestamp',
                        TIMESTAMP(timezone=False),
                        nullable=False,
                        server_default=text("NOW()"),
                        )

class Vote(database.Base):
    __tablename__ = "votes"
    user_id = Column(Integer,
                     ForeignKey("users.id",ondelete="CASCADE"),
                     primary_key=True)
    post_id = Column(Integer,
                     ForeignKey("posts.id", ondelete="CASCADE"),
                     primary_key=True)
