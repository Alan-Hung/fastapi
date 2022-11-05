from app import schemas, database, models, crud, utils, oauth2
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

Router = APIRouter(tags=["Authentication"])

@Router.post("/login", response_model=schemas.Token)
def login(login_info: OAuth2PasswordRequestForm=Depends(), db=Depends(database.get_db)):
    email, password = login_info.username, login_info.password
    user = crud.get_user_with_email(db=db, model=models.User, email=email)
    if user is None or not utils.verify(password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                    detail="Incorrect password or email",
                    )
    # Create token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}