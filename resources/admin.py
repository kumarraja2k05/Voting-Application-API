import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from db import db
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from models import AdminModel
from schemas import PlainAdminSchema

blp=Blueprint("admin",__name__,description="Operations on Admin")

# admin_details={}

@blp.route("/admin_details")
class Admin(MethodView):
    @blp.response(200,PlainAdminSchema(many=True))
    def get(self):
        # return {"admin_details": list(admin_details.values())} 
        return AdminModel.query.all()

    @blp.arguments(PlainAdminSchema)
    @blp.response(200,PlainAdminSchema)
    def post(self,admin_data):
        admin=AdminModel(**admin_data)
        try:
            db.session.add(admin)
            db.session.commit()
        except IntegrityError as e:
            print("Error of Admin{}".format(e))
            abort(400,message="Admin with that name already exists.")
        except SQLAlchemyError:
            abort(500,message="An Error occured creating the Admin.")
        return admin

        # admin_data=request.get_json()
        # admin_id= uuid.uuid4().hex
        # new_details={**admin_data,"id": admin_id}
        # admin_details[admin_id]=new_details
        # return new_details


