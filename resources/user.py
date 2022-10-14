import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from models import UserModel
from flask_jwt_extended import jwt_required
from db import db
from schemas import PlainUserSchema,UserUpdateSchema

blp=Blueprint("user",__name__,description="Operations on Users")

# user_details={}

@blp.route("/user_details")
class User(MethodView):
    @jwt_required()
    @blp.response(200,PlainUserSchema(many=True))
    def get(self):
        try:
            # return {"user_details":list(user_details.values())}
            return UserModel.query.all()
        except KeyError:
            abort(404,message="Item not found.")

    @jwt_required()
    @blp.arguments(PlainUserSchema)  
    @blp.response(201,PlainUserSchema) 
    def post(self,user_data):
        # user_data=request.get_json()

        user=UserModel(**user_data)
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            print("Error {}".format(e))
            abort(500,message="An Error occured while inserting the item.")
        return user
        
        # user_id= uuid.uuid4().hex
        # new_details={**user_data,"id": user_id}
        # user_details[user_id]=new_details
        # return new_details

@blp.route("/user_details/<string:id>")
class UserPutDelete(MethodView):
    @jwt_required()
    def delete(self,id):
        user=UserModel.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return {"message":"User deleted"}
        # try:
        #     del user_details[id]
        #     return {"message":"Item Deleted"}
        # except KeyError:
        #     return {"message":"Item Not found"},404

    @blp.arguments(UserUpdateSchema)
    @blp.response(200,PlainUserSchema)
    def put(self,user_data,id):
        user=UserModel.query.get(id)
        if user:
            user.name=user_data["name"]
            user.contact=user_data["contact"]
            user.email=user_data["email"]
        else:
            user=UserModel(user_id=id,**user_data)

        db.session.add(user)
        db.session.commit()
        return user

        # user_data=request.get_json()
        # if "name" not in user_data or "phone" not in user_data or "email" not in user_data:
        #     return {"message":"BadRequest. Ensure 'name' and 'place' are in JSON payload"}, 400
        # try:
        #     detail=user_details[id]
        #     detail |= user_data
        #     return detail

        # except KeyError:
        #     return {"meassage":"Item Not found"}, 404


