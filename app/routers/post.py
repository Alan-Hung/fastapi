from app import schemas, database, models, crud, oauth2
from typing import List, Optional
from fastapi import Depends, HTTPException, status, APIRouter
import pdb

Router = APIRouter(prefix="/posts", tags=["Posts"])


@Router.get("/",
            response_model=List[schemas.PostWithVote],
            )
def get_posts(db=Depends(database.get_db),
              skip: int = 0,
              limit: int = 100,
              current_user=Depends(oauth2.get_current_user),
              title_contain: str = "",
              ):
    posts = crud.get_posts_with_votes(db=db,
                                      skip=skip,
                                      limit=limit,
                                      title_contain=title_contain,
                                      )
    return posts


@Router.get("/{post_id}", response_model=schemas.Post)
def get_post(post_id: int,
             db=Depends(database.get_db),
             current_user=Depends(oauth2.get_current_user),
             ):
    # pdb.set_trace()
    post = crud.get_row(db=db, model=models.Post, id_=post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id={post_id} is not found.",
                            )
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="Not authorized to perform requested action.",
    #                         )
    return post


@Router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.CreatePost,
             )
def create_post(post: schemas.PostBase,
                db=Depends(database.get_db),
                current_user=Depends(oauth2.get_current_user),
                ):
    return crud.create(db=db, model=models.Post, schema=post, owner_id=current_user.id)


@Router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int,
                db=Depends(database.get_db),
                current_user=Depends(oauth2.get_current_user),
                ):
    post_exist = get_post(post_id, db, current_user)
    if post_exist:
        crud.delete_post(db, post_id)


@Router.put("/{post_id}", response_model=schemas.UpdatePost)
def update_post(post_id: int,
                post: schemas.UpdatePost,
                db=Depends(database.get_db),
                current_user=Depends(oauth2.get_current_user),
                ):
    post_exist = get_post(post_id, db, current_user)
    if post_exist:
        crud.update_post(db, post_id, post)
        return post_exist
