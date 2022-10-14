from flask import Flask,jsonify
from flask_smorest import abort,Api
from db import db
from flask_jwt_extended import JWTManager
from models import UserModel
from sqlalchemy.exc import SQLAlchemyError
from resources.user_auth import blp as UserAuthBlueprint
from resources.user import blp as UserBlueprint
from resources.admin import blp as AdminBlueprint
import os

def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPOGATE_EXCEPTIONS"]=True
    app.config["API_TITLE"]="Stores REST API"
    app.config["API_VERSION"]="v1"
    app.config["OPENAPI_VERSION"]="3.0.3"
    app.config["OPENPI_URL_PREFIX"]="/"
    app.config["OPENAPI_SWAGGER_UI_PATH"]="/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"]="https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"]=db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    db.init_app(app)

    app.config["JWT_SECRET_KEY"]="245964595290064766420054926723820826002"
    jwt=JWTManager(app)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header,jwt_payload):
        return (jsonify({"message":"The token expired","error":"token_expired"}), 401,)

    @jwt.invalid_token_loader
    def invalid_token_callbacks(error):
        return (jsonify({"message":"Signature verification failed.","error":"invalid_token"}),401,)

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return(jsonify({
            "description":"Request does not contain an access token.",
            "error": "authorization_required",
        }),401,)

    api=Api(app)
    
    @app.before_first_request
    def create_tables():
        db.create_all()

    api.register_blueprint(UserAuthBlueprint)
    api.register_blueprint(AdminBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
    
#details=[{"id": 2,"details":[{"name":"Raja","DOB":"2000-10-05","phone":147896325}]}]

# admin_details={}
# user_details={}

# @app.get("/admin_details")
# def get_admin_details():
#     return {"admin_details": list(admin_details.values())} 


# @app.get("/user_details")
# def get_user_details():
#     return {"user_details":list(user_details.values())}

# @app.post("/admin_details")
# def admin_add_deatils():
#     admin_data=request.get_json()
#     admin_id= uuid.uuid4().hex
#     new_details={**admin_data,"id": admin_id}
#     admin_details[admin_id]=new_details
#     return new_details, 201

# @app.post("/user_details")
# def user_add_details():
#     user_data=request.get_json()
#     # user=UserModel(**user_data)
#     # try:
#     #     db.session.add(user)
#     #     db.session.commit()
#     # except SQLAlchemyError:
#     #     abort(500,message="An Error occured while inserting the item.")
#     # return user
    
#     user_id= uuid.uuid4().hex
#     new_details={**user_data,"id": user_id}
#     user_details[user_id]=new_details
#     return new_details, 201

# @app.delete("/user_details/<string:id>")
# def delete_data(id):
#     try:
#         del user_details[id]
#         return {"message":"Item Deleted"}
#     except KeyError:
#         return {"message":"Item Not found"},404

# @app.put("/user_details/<string:id>")
# def update_item(id):
#     user_data=request.get_json()
#     if "name" not in user_data or "phone" not in user_data or "email" not in user_data:
#         return {"message":"BadRequest. Ensure 'name' and 'place' are in JSON payload"}, 400
#     try:
#         detail=user_details[id]
#         detail |= user_data
#         return detail

#     except KeyError:
#         return {"meassage":"Item Not found"}, 404

