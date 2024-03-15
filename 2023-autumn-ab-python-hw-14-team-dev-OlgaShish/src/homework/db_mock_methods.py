from typing import Any, Optional
from sqlalchemy.orm import Session
from src.homework.tps import User, Post, Tags, Comment
from src.homework.db.tables import (
    Users,
    Posts,
    UsersPosts,
    Comments,
    Tags as TagsTable,
)


def add_user(session: Session, user: User) -> Any:
    db_user = Users(
        login=user.login,
        password=user.password,
        first_name=user.first_name,
        second_name=user.second_name,
        is_admin=user.is_admin,
        skills="|".join(user.skils),
        company=user.company,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user.id


def find_user(session: Session, user_id: Any) -> Optional[User]:
    db_user = session.query(Users).filter(Users.id == user_id).first()
    if db_user is None:
        return None

    query_result = (
        session.query(UsersPosts.post_id, Posts.name)
        .join(Posts, UsersPosts.post_id == Posts.id)
        .filter(UsersPosts.user_id == user_id)
        .all()
    )
    post_dict = {result.post_id: result.name for result in query_result}
    return User(
        user_id=db_user.id,
        login=db_user.login,
        password=db_user.password,
        first_name=db_user.first_name,
        second_name=db_user.second_name,
        is_admin=db_user.is_admin,
        skils=db_user.skills.split("|"),
        company=db_user.company,
        posts_ids_to_names=post_dict,
        tohash=False,
    )


def find_user_by_login(session: Session, user_login: str) -> Optional[User]:
    db_user = session.query(Users).filter(Users.login == user_login).first()
    if db_user is None:
        return None

    query_result = (
        session.query(UsersPosts.post_id, Posts.name)
        .join(Posts, UsersPosts.post_id == Posts.id)
        .filter(UsersPosts.user_id == db_user.id)
        .all()
    )
    post_dict = {result.post_id: result.name for result in query_result}
    return User(
        user_id=db_user.id,
        login=db_user.login,
        password=db_user.password,
        first_name=db_user.first_name,
        second_name=db_user.second_name,
        is_admin=db_user.is_admin,
        skils=db_user.skills.split("|"),
        company=db_user.company,
        posts_ids_to_names=post_dict,
        tohash=False,
    )


def add_or_update_post(session: Session, post: Post) -> Any:
    existing_post = (
        session.query(Posts)
        .filter(Posts.author_id == post.author_id, Posts.name == post.name)
        .first()
    )

    if existing_post:
        existing_post.likes = post.likes
        existing_post.dislikes = post.dislikes
    else:
        db_post = Posts(
            name=post.name,
            text=post.text,
            author_id=post.author_id,
            likes=post.likes,
            dislikes=post.dislikes,
            time=post.time,
        )
        session.add(db_post)
        session.commit()
        session.refresh(db_post)
        existing_post = db_post

        for tag in post.tags:
            db_tag = TagsTable(post_id=existing_post.id, type=tag.name)
            session.add(db_tag)

    for comment in post.comments:
        if comment.comment_id is None:
            db_comment = Comments(
                user_id=comment.user_id,
                post_id=existing_post.id,
                user_name=comment.user_name,
                text=comment.text,
                time=comment.time,
            )
            session.add(db_comment)

    session.commit()
    return existing_post.id


def find_post(session: Session, post_id: Any) -> Optional[Post]:
    db_post = session.query(Posts).filter(Posts.id == post_id).first()
    if db_post is None:
        return None

    comments = get_comments_by_post_id(session, post_id)
    tags = get_tags_by_post_id(session, post_id)

    return Post(
        post_id=db_post.id,
        name=db_post.name,
        text=db_post.text,
        author_id=db_post.author_id,
        tags=tags,
        comments=comments,
        likes=db_post.likes,
        dislikes=db_post.dislikes,
        time=db_post.time,
    )


def add_post_id_to_user(session: Session, post_id: Any, user_id: Any) -> None:
    db_user_post = UsersPosts(user_id=user_id, post_id=post_id)
    session.add(db_user_post)
    session.commit()


def get_posts(
    session: Session,
    author_id: Any,
    tags: list[Tags],
    name_search: Optional[str],
    pagination: int,
) -> list[Post]:
    query = session.query(Posts)

    if author_id is not None:
        query = query.filter(Posts.author_id == author_id)
    elif tags:
        tag_names = [tag.name for tag in tags]
        query = (
            query.join(TagsTable, Posts.id == TagsTable.post_id)
            .filter(TagsTable.type.in_(tag_names))
            .distinct()
        )
    elif name_search is not None:
        query = query.filter(Posts.name.ilike(f"%{name_search}%"))

    result = query.offset(pagination * 10).limit(10).all()

    posts = []
    for post in result:
        tags = get_tags_by_post_id(session, post.id)
        comments = get_comments_by_post_id(session, post.id)
        posts.append(
            Post(
                post_id=post.id,
                name=post.name,
                text=post.text,
                author_id=post.author_id,
                tags=tags,
                comments=comments,
                likes=post.likes,
                dislikes=post.dislikes,
                time=post.time,
            )
        )

    return posts


def get_tags_by_post_id(session: Session, post_id: int) -> list[Tags]:
    db_tags = (
        session.query(TagsTable).filter(TagsTable.post_id == post_id).all()
    )
    tags = [Tags[tag.type] for tag in db_tags]
    return tags


def get_comments_by_post_id(session: Session, post_id: int) -> list[Comments]:
    db_comments = (
        session.query(Comments).filter(Comments.post_id == post_id).all()
    )
    comments = [
        Comment(
            user_id=comment.user_id,
            post_id=comment.post_id,
            user_name=comment.user_name,
            text=comment.text,
            time=comment.time,
        )
        for comment in db_comments
    ]
    return comments


def delete_post(session: Session, post_id: Any) -> None:
    session.query(UsersPosts).filter(UsersPosts.post_id == post_id).delete()
    session.query(TagsTable).filter(TagsTable.post_id == post_id).delete()
    session.query(Comments).filter(Comments.post_id == post_id).delete()
    session.query(Posts).filter(Posts.id == post_id).delete()
    session.commit()
