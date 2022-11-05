from app import schemas, database, models, crud, utils, oauth2
from fastapi import Depends, HTTPException, status, APIRouter
from app.routers import post

Router = APIRouter(prefix="/votes", tags=["Votes"])


@Router.post("/", status_code=status.HTTP_201_CREATED)
def add_vote(vote: schemas.Vote,
             db=Depends(database.get_db),
             current_user=Depends(oauth2.get_current_user),
             ):
    post_id = vote.post_id
    user_id = current_user.id
    # Retrieve the post with post_id, and check if post exist.
    _ = post.get_post(post_id, db, current_user)
    # Retrieve votes result from vote table (model.Vote)
    vote_result = crud.get_vote(db=db,
                                model=models.Vote,
                                post_id=post_id,
                                user_id=user_id)
    if vote_result is not None and vote.direction == 1:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"user {user_id} has already voted on post {vote.post_id}")
    if vote_result is None and vote.direction == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Vote does not exist")
    if vote.direction == 1:
        crud.add_vote(db=db,
                      model=models.Vote,
                      user_id=user_id,
                      post_id=post_id)
        return {"message": "add vote successfully"}
    if vote.direction == 0:
        crud.delete_vote(db=db, post_id=post_id, user_id=user_id)
        return {"message": "delete vote successfully"}
