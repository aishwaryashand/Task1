from pydantic import BaseModel


class UserInfoBase(BaseModel):
    username: str


class UserCreate(UserInfoBase):
    fullname: str
    password: str


class UserAuthenticate(UserInfoBase):
    password: str


class UserInfo(UserInfoBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class BlogBase(BaseModel):
    title: str
    content: str


class Blog(BlogBase):
    id: int

    class Config:
        orm_mode = True


class RequestResponseBase(BaseModel):
    univ_id:int
    roll_no:str
    response_url:str= None
    dob:str
    status:int= None
    sem:str=None


class RequestResponse(RequestResponseBase):
    request_id: int

    class Config:
        orm_mode = True        
