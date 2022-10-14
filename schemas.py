from marshmallow import Schema,fields

class PlainUserSchema(Schema):
    user_id=fields.Int(dump_only=True)
    name=fields.Str(required=True)
    fathers_name=fields.Str(required=True)
    aadhar_number=fields.Int(required=True)
    dob=fields.Date(required=True)
    contact=fields.Int(required=True)
    email=fields.Str(required=True)
    pswd=fields.Int(required=True)

class PlainAdminSchema(Schema):
    admin_id=fields.Int(dump_only=True)
    name=fields.Str(required=True)
    fathers_name=fields.Str(required=True)
    aadhar_number=fields.Int(required=True)
    dob=fields.Date(required=True)
    contact=fields.Int(required=True)
    email=fields.Str(required=True)
    pswd=fields.Int(required=True)

class UserUpdateSchema(Schema):
    name=fields.Str()
    contact=fields.Int()
    email=fields.Str()

class UserAuthSchema(Schema):
    id=fields.Int(dump_only=True)
    username=fields.Str(required=True)
    password=fields.Str(reured=True)

