from sqlalchemy.orm import Session
from sqlalchemy import delete, update, func
from app import models, schemas, database
import pydantic


def create(db: Session, model: database.Base, schema: pydantic.BaseModel, **kwargs):
    # create(db: Session, post:schemas.CreatePost, model:database.Base):
    update_schema = schema.dict()
    update_schema.update(kwargs)
    new = model(**update_schema)
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


def get_rows(db: Session,
             model: database.Base,
             skip: int = 0,
             limit: int = 100,
             title_contain: str = "",
             ):
    return (db
            .query(model)
            .filter(models.Post.title.contains(title_contain))
            .offset(skip)
            .limit(limit)
            .all())

# posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        # models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

def get_row(db: Session,
            model: database.Base,
            id_: int,
            ):
    return db.query(model).filter(model.id == id_).first()


def get_user_with_email(db: Session, model: database.Base, email: str):
    return db.query(model).filter(model.email == email).first()


def delete_post(db: Session, post_id: int):
    stmt = (delete(models.Post)
            .where(models.Post.id == post_id)
            )
    print(stmt)
    db.execute(stmt)
    db.commit()


def update_post(db: Session, post_id: int, post: schemas.UpdatePost):
    stmt = (update(models.Post)
            .where(models.Post.id == post_id)
            # .values(title=post.title, content=post.content)
            .values(**post.dict())
            )
    db.execute(stmt)
    db.commit()


def get_vote(db: Session, model: database.Base, post_id: int, user_id: int):
    return (db.query(model)
            .filter(model.post_id == post_id,
                    model.user_id == user_id,
                    )
            .first())


def add_vote(db: Session, model: database.Base, user_id: int, post_id: int):
    new = model(user_id=user_id, post_id=post_id)
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


def delete_vote(db: Session, post_id: int, user_id: int):
    stmt = (delete(models.Vote)
            .where(models.Vote.post_id == post_id, models.Vote.user_id == user_id)
            )
    db.execute(stmt)
    db.commit()


def get_posts_with_votes(db: Session,
                         skip: int = 0,
                         limit: int = 100,
                         title_contain: str = "",
                         ):
    return (db
            .query(models.Post, func.count(models.Vote.post_id).label("votes"))
            .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
            .group_by(models.Post.id)
            .filter(models.Post.title.contains(title_contain))
            .limit(limit).offset(skip)
            .all())
