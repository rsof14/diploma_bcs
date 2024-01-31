from marshmallow import Schema, fields, validate


class LoginIn(Schema):
    login = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(max=50))


class LoginOut(Schema):
    access_token = fields.Str(required=True)
    refresh_token = fields.Str(required=True)


login_in = LoginIn()
login_out = LoginOut()