import datetime
from sqlalchemy import Column, Integer, String, DateTime
from database import Base


class UserInfo(Base):
    __tablename__ = "user_info"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(200), unique=True,)
    password = Column(String(200))
    fullname = Column(String(100), unique=True)


class Blog(Base):
    __tablename__ = "blog"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    content = Column(String(100))

class ApiInput(Base):
    __tablename__="api_input"

    id = Column(Integer, primary_key=True, index=True)
    univ_id = Column(Integer)
    params = Column(String(200))
    status=Column(Integer)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)


class RequestResponse(Base):
    __tablename__="api_request_response"

    request_id = Column(Integer, primary_key=True, index=True)
    univ_id = Column(Integer)
    roll_no = Column(String(200))
    dob = Column(String(100))
    response_url = Column(String(200))
    request_data = Column(String(1000))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)





