from fastapi import FastAPI, Response, status, HTTPException,Depends
from dataclasses import dataclass, asdict
import random
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from app import models, database
from app import schemas

# Create all models (i.e. tables)
models.database.Base.metadata.create_all(bind=database.Engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host="localhost",
                                database="fastapi",
                                user="postgres",
                                cursor_factory=RealDictCursor
                                )
        cursor = conn.cursor()
        print("Connect to database successfully.")
        break
    except psycopg2.OperationalError:
        print("Connection failed")
        time.sleep(2)


def find_post(post_id: int, db: str):
    cursor.execute(f"SELECT * FROM {db} WHERE id=%s", (str(post_id),))
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id={post_id} is not found.",
                            )
    return post

@app.get("/")
async def root():
    return {"message": "abc"}


@app.get("/posts")
def get_posts(db: str = "posts"):
    cursor.execute(f"SELECT * FROM {db}")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.Post, db: str = "posts"):
    cursor.execute(f"INSERT INTO {db} (title, content, published)"
                   "VALUES (%s, %s, %s) RETURNING *",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{post_id}")
def get_post(post_id: int, db: str = "posts"):
    post = find_post(post_id, db)
    return {"data": post}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: str = "posts"):
    post = find_post(post_id, db)
    if post is not None:
        cursor.execute(f"DELETE FROM {db} WHERE id=%s", str(post_id))
        conn.commit()
        print(f"post {post_id} deleted")

@app.put("/posts/{post_id}")
def update_post(post_id: int, post: schemas.Post, db: str = "posts"):
    # find post
    post_ = find_post(post_id, db)
    # SQL command
    update = f"UPDATE {db}"
    change, attribute = [], []
    for keys, values in post.dict().items():
        if values is not None:
            columns = "".join([keys, " = %s"])
            change.append(columns)
            attribute.append(keys)
    post_change = " SET " + ",".join(change)
    attr_change = [getattr(post,attr) for attr in attribute]
    attr_change.append(str(post_id))

    # Update post
    updated_post = None
    if post_ is not None:
        cursor.execute(update + post_change + " WHERE id=%s RETURNING *",
                       attr_change
                       )
        updated_post = cursor.fetchone()
        conn.commit()
    return {"data": updated_post}

