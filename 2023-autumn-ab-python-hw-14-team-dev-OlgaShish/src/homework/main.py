from typing import Any
from fastapi import Depends, FastAPI, HTTPException
import json

from sqlalchemy.orm import Session
from src.homework import models
import src.homework.tkn as token
import src.homework.tps as types
import src.homework.db_mock_methods as db
from src.homework.db import tables
from src.homework.db.database import engine, SessionLocal

tables.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.post("/registration")
async def registration(
    user: models.User, session: Session = Depends(get_session)
):
    db_user = types.User(
        login=user.login,
        password=user.password,
        first_name=user.first_name,
        second_name=user.second_name,
        is_admin=False,
        skils=user.skils,
        company=user.company,
        posts_ids_to_names={},
    )
    user_id = db.add_user(session, db_user)
    jwt_token = token.make_token(user_id)
    return jwt_token


@app.post("/authentication")
async def authentication(
    user_info: models.UserInfoAuth, session: Session = Depends(get_session)
):
    user = db.find_user_by_login(session, user_info.login)
    if user is None:
        raise HTTPException(status_code=400, detail="Bad login")
    if user.password != hash(user_info.password):
        raise HTTPException(status_code=400, detail="Bad password")
    jwt_token = token.make_token(user.user_id)
    return jwt_token


@app.post("/authorization")
async def authorization(
    user_info: models.UserInfo, session: Session = Depends(get_session)
):
    user_token = user_info.token
    jwt_token = token.read_token(user_token)
    try:
        if token.is_token_need_refresh(user_token):
            user_id = jwt_token["user_id"]
            new_token = token.make_token(user_id)
        else:
            user_id = jwt_token["user_id"]
            new_token = user_token
    except token.BadToken:
        raise HTTPException(
            status_code=400, detail="Bad token, you are very suspicious"
        )
    user = db.find_user(session, user_id)
    if user is None or user.login != user_info.login:
        raise HTTPException(status_code=400, detail="Bad login")
    if user.password != hash(user_info.password):
        raise HTTPException(status_code=400, detail="Bad password")
    return new_token


async def get_token(user_token: str) -> Any:
    try:
        if token.is_token_need_refresh(user_token):
            raise HTTPException(
                status_code=400, detail="Bad token, you need relogin"
            )
        return token.read_token(user_token)["user_id"]
    except token.BadToken:
        raise HTTPException(
            status_code=400, detail="Bad token, you are very suspicious"
        )


@app.post("/create_post")
async def create_post(
    post: models.CreateOrUpdatePost, session: Session = Depends(get_session)
):
    user_id = await get_token(post.token)
    db_post = types.Post(
        name=post.name,
        text=post.text,
        author_id=user_id,
        tags=post.tags,
        comments=[],
        likes=0,
        dislikes=0,
    )
    post_id = db.add_or_update_post(session, db_post)
    db.add_post_id_to_user(session, post_id, user_id)


@app.post("/update_post")
async def update_post(
    post: models.CreateOrUpdatePost, session: Session = Depends(get_session)
):
    user_id = await get_token(post.token)
    if post.post_id is None:
        raise HTTPException(status_code=400, detail="No post id")
    db_post = db.find_post(session, post.post_id)
    if db_post is None:
        raise HTTPException(status_code=400, detail="No post with such id")
    db_user = db.find_user(session, user_id)
    if db_post is None:
        raise HTTPException(status_code=400, detail="No user with such id")
    comments = db_post.comments
    for comment in post.new_comments:
        comments.append(
            types.Comment(user_id, post.post_id, db_user.first_name, comment)
        )
    likes = db_post.likes
    if post.new_likes is not None:
        likes = post.new_likes
    dislikes = db_post.dislikes
    if post.new_dislikes is not None:
        dislikes = post.new_dislikes
    db_post = types.Post(
        name=post.name,
        text=post.text,
        author_id=db_post.author_id,
        tags=post.tags,
        comments=comments,
        likes=likes,
        dislikes=dislikes,
    )
    db.add_or_update_post(session, db_post)


@app.post("/delete_post")
async def delete_post(
    post: models.DeletePost, session: Session = Depends(get_session)
):
    user_id = await get_token(post.token)
    db_post = db.find_post(session, post.post_id)
    if db_post is None:
        raise HTTPException(status_code=400, detail="No post with such id")
    if user_id != str(db_post.author_id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    db.delete_post(session, post.post_id)


@app.post("/get_posts")
async def get_posts(
    posts_info: models.GetPosts, session: Session = Depends(get_session)
):
    with open("config.json", encoding="utf-8") as config:
        pagination_size = json.load(config)["pagination"]
    posts = db.get_posts(
        session,
        posts_info.author_id,
        posts_info.tags,
        posts_info.name_search,
        posts_info.pagination_current,
    )
    return {
        "posts": posts,
        "new_pagination": posts_info.pagination_current + pagination_size,
    }
