from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(Integer, nullable=False)
    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    skills = Column(String, default="")
    company = Column(String)


class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    text = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    time = Column(DateTime, nullable=False)

    user = relationship("Users", back_populates="posts")


class UsersPosts(Base):
    __tablename__ = "usersposts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)

    user = relationship("Users", back_populates="user_posts")
    post = relationship("Posts", back_populates="post_users")


class Comments(Base):
    __tablename__ = "comments"

    comment_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_name = Column(String, nullable=False)
    text = Column(String, nullable=False)
    time = Column(DateTime, nullable=False)

    user = relationship("Users", back_populates="comments")
    post = relationship("Posts", back_populates="comments")


class Tags(Base):
    __tablename__ = "tags"

    tag_id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    type = Column(String, nullable=False)

    post = relationship("Posts", back_populates="tags")


Users.posts = relationship("Posts", back_populates="user")
Users.comments = relationship("Comments", back_populates="user")
Posts.comments = relationship("Comments", back_populates="post")
Posts.tags = relationship("Tags", back_populates="post")
Users.user_posts = relationship("UsersPosts", back_populates="user")
Posts.post_users = relationship("UsersPosts", back_populates="post")
