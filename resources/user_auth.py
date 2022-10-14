from os import access
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from passlib.hash import pbkdf2_sha256
from db import db
from flask_jwt_extended import create_access_token
from models import UserAuthModel
from schemas import UserAuthSchema

blp=Blueprint("UserAuth","userAuth", description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserAuthSchema)
    def post(self,user_data):
        if UserAuthModel.query.filter(UserAuthModel.username==user_data["username"]).first():
            abort(409,message="A user with that username already exsits.")

        user=UserAuthModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        db.session.add(user)
        db.session.commit()

        return {"message":"User created successfully."}, 201

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserAuthSchema)
    def post(self,user_data):
        user=UserAuthModel.query.filter(
            UserAuthModel.username == user_data["username"]
        ).first()
        if user and pbkdf2_sha256.verify(user_data["password"],user.password):
            access_token= create_access_token(identity=user.id)
            return {"access_token": access_token}

        abort(401,message="Invalid Credentials.")

@blp.route("/user/<int:user_id>")    
class UserGetDelete(MethodView):
    @blp.response(200,UserAuthSchema)
    def get(self,user_id):
        user=UserAuthModel.query.get_or_404(user_id)
        return user

    def delete(self,user_id):
        user=UserAuthModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"essage":"User delete."},200

        