from sqlalchemy.orm import Session
import models, schemas
import bcrypt
import json
import pandas

def get_user_by_username(db: Session, username: str):
    return db.query(models.UserInfo).filter(models.UserInfo.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = models.UserInfo(username=user.username, password=hashed_password, fullname=user.fullname)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def check_username_password(db: Session, user: schemas.UserAuthenticate):
    db_user_info: models.UserInfo = get_user_by_username(db, username=user.username)
    return bcrypt.checkpw(user.password.encode('utf-8'), db_user_info.password.encode('utf-8'))


def create_new_blog(db: Session, blog: schemas.BlogBase):
    db_blog = models.Blog(title=blog.title, content=blog.content)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog


def get_all_blogs(db: Session):
    return db.query(models.Blog).all()


def get_blog_by_id(db: Session, blog_id: int):
    return db.query(models.Blog).filter(models.Blog.id == blog_id).first()


def get_params_by_univ_id(db:Session,univ_id:int):
    return db.query(models.ApiInput).filter(models.ApiInput.univ_id==univ_id).all()


def create_new_request_response(db: Session, api_resuest: schemas.RequestResponseBase):
    data = pandas.DataFrame(api_resuest)
    db_api_resuest = models.RequestResponse(univ_id=api_resuest.univ_id, roll_no=api_resuest.roll_no,dob=api_resuest.dob,request_data=str(data.set_index(0).to_dict()[1]), response_url=api_resuest.response_url)
    db.add(db_api_resuest)
    db.commit()
    db.refresh(db_api_resuest)
    return db_api_resuest
