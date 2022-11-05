from app import schemas, database, models, crud, utils
from typing import List
from fastapi import Depends, HTTPException, status, APIRouter

Router = APIRouter(prefix="/users", tags=["Users"])

@Router.post("/")
def create_user(user: schemas.User, db=Depends(database.get_db)):
    user.password = utils.hash(user.password)
    return crud.create(db=db, model=models.User, schema=user)

@Router.get("/", response_model=List[schemas.User])
def get_users(db=Depends(database.get_db), skip: int = 0, limit: int = 100):
    users = crud.get_rows(db=db, model=models.User, skip=skip, limit=limit)
    return users

@Router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id:int, db=Depends(database.get_db)):
    user = crud.get_row(db=db, model=models.User, id_=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id={user_id} is not found.",
                            )
    return user
