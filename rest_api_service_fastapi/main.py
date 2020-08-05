import uvicorn
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException,Request
from starlette import status

import crud
import models
import schemas
from app_utils import decode_access_token
from crud import get_user_by_username
from database import engine, SessionLocal
from schemas import UserInfo, TokenData, UserCreate, Token,RequestResponse

models.Base.metadata.create_all(bind=engine)

ACCESS_TOKEN_EXPIRE_MINUTES = 1000

app = FastAPI()


# Dependency


def get_db():
	db = None
	try:
		db = SessionLocal()
		yield db
	finally:import requests
	db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authenticate")


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(data=token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except PyJWTError:
        raise credentials_exception
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/user", response_model=UserInfo)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


@app.post("/authenticate", response_model=Token)
def authenticate_user(user: schemas.UserAuthenticate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Username not existed")
    else:
        is_password_correct = crud.check_username_password(db, user)
        if is_password_correct is False:
            raise HTTPException(status_code=400, detail="Password is not correct")
        else:
            from datetime import timedelta
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            from app_utils import create_access_token
            access_token = create_access_token(
                data={"sub": user.username}, expires_delta=access_token_expires)
            return {"access_token": access_token, "token_type": "Bearer"}


@app.post("/blog", response_model=schemas.Blog)
async def create_new_blog(blog: schemas.BlogBase, current_user: UserInfo = Depends(get_current_user), db: Session = Depends(get_db)):
    yy= crud.create_new_blog(db=db, blog=blog)
    print(type(yy))
    exit


@app.get("/blog")
async def get_all_blogs(current_user: UserInfo = Depends(get_current_user)
                        , db: Session = Depends(get_db)):
    return crud.get_all_blogs(db=db)


@app.get("/blog/{blog_id}")
async def get_blog_by_id(blog_id, current_user: UserInfo = Depends(get_current_user)
                         , db: Session = Depends(get_db)):
    return crud.get_blog_by_id(db=db, blog_id=blog_id)


@app.get("/apiparams/{univ_id}")
async def get_api_params_by_univ_id(univ_id,current_user:UserInfo=Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.get_params_by_univ_id(db=db,univ_id=univ_id)

import pandas
@app.post("/getResult",response_model=RequestResponse,response_model_exclude_unset=True)
async def create_new_request_response(request: schemas.RequestResponseBase,current_user:UserInfo=Depends(get_current_user),db:Session=Depends(get_db)):

    db_data = crud.get_params_by_univ_id(db=db,univ_id=request.univ_id)
    db_params = []
    for x in db_data:
        db_params.append(x.params)
    
    sem_err = None
    request_data = (pandas.DataFrame(request)).set_index(0).to_dict()[1]
    request_params = request_data.keys()
    for x in db_params:
        if (x in request_params and request_data[x] != None):
            if 'sem' in db_params:
                sem_err = request.sem
        else:
            sem_err = "Missing field sem"

    module = __import__(str(request.univ_id))
    path,response = module.login(request)
    request.response_url = path
    result=crud.create_new_request_response(db=db, api_resuest=request)
    if sem_err != None :
        result.sem = sem_err
    return result


  #print(type(yy))
  #exit
  #request_dict_key=json_param.keys()
  #univ_id=json_param['univ_id']
  #return crud.create_new_request_response(db=db, api_resuest=yyy)  

  #=crud.get_params_by_univ_id(db=db,univ_id=univ_id)
  #return input_params
  #print(type(input_params))
  #exit
  #database_key={}
  #i=0
 # for record in input_params:
 #     database_key[record.params]=i
  #    i=i+1

  #database_dict_key=database_key.keys()
  #value = { k : database_dict_key[k] for k in set(database_dict_key) - set(request_dict_key) }
  #print(value)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
