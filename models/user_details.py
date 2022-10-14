from db import db

class UserModel(db.Model):
    __tablename__="user"

    user_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),unique=True,nullable=False)
    fathers_name=db.Column(db.String(100),unique=True,nullable=False)
    aadhar_number=db.Column(db.Integer,unique=True,nullable=False)
    dob=db.Column(db.Date,unique=False,nullable=False)
    contact=db.Column(db.Integer,unique=True,nullable=False)
    email=db.Column(db.String(100),unique=True,nullable=False)
    pswd=db.Column(db.Integer,unique=False,nullable=False)