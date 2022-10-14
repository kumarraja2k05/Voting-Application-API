from flask import Flask,request
from flask_smorest import abort
from flask_jwt_extended import JWTManager
import uuid

app = Flask(__name__)

app.config["JWT_SECRET_KEY"]="73406063808092994757625407243404042365"
jwt=JWTManager(app)

elections={}
voting={}
#details=[{"id": 2,"details":[{"name":"Raja","DOB":"2000-10-05","phone":147896325}]}]
@app.get("/elections")
def get_election_details():
    return {"election details": list(elections.values())}
    

@app.get("/voting")
def get_voting_details():
    #return {"election_details": details}
    return {"Voting details": list(voting.values())}

@app.post("/elections")
def create_elections():
    election_data=request.get_json()
    election_id= uuid.uuid4().hex
    new_details={**election_data,"id": election_id}
    elections[election_id]=new_details
    return new_details, 201

@app.post("/voting")
def create_voting():
    voting_data=request.get_json()
    if voting_data["election_id"] not in elections:
        return {"message":"Election not found"}, 404

    voting_id=uuid.uuid4().hex
    new_data={**voting_data,"id":voting_id}
    voting[voting_id]=new_data
    return new_data, 201

@app.delete("/voting/<string:id>")
def delete_data(id):
    try:
        del voting[id]
        return {"message":"Item Deleted"}
    except KeyError:
        return {"message":"Item Not found"},404

@app.put("/voting/<string:id>")
def update_item(id):
    voting_data=request.get_json()
    if "parties" not in voting_data or "votes" not in voting_data:
        return {"message":"BadRequest. Ensure 'parties' and 'vote' are in JSON payload"}, 400
    try:
        new_detail=voting[id]
        new_detail |= voting_data
        return new_detail

    except KeyError:
        return {"meassage":"Item Not found"}, 404 