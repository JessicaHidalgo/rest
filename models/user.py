from flask_login import UserMixin 
from datetime import datetime
from sqlalchemy.orm import relationship 
from . import db
from .enums import UserStatus
class User(db.Model,UserMixin):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer,primary_key= True)
    first_name = db.Column(db.String(length=50),nullable=False)
    status = db.Column(db.Enum(UserStatus),nullable=False)
