from marshmallow import Schema, fields, validate

from api.v1.models.common import PaginateOut
from api.v1.models.marshmallow_init import ma
from db.models import LoginHistory as LoginHistoryModel


class UsersSchema(Schema):
    name = fields.Str(validate=validate.Length(max=100))
    login = fields.Str(validate=validate.Length(max=50))
    role_id = fields.UUID()
    role = fields.Str(validate=validate.Length(max=100))
    created_at = fields.DateTime()


class ChangePassword(Schema):
    old_password = fields.Str(required=True, validate=validate.Length(max=50))
    new_password = fields.Str(required=True, validate=validate.Length(max=50))
    new_password_again = fields.Str(required=True, validate=validate.Length(max=50))


class LoginHistory(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LoginHistoryModel


class LoginHistoryPaginated(ma.Schema):
    results = fields.Nested(LoginHistory, many=True)
    pagination = fields.Nested(PaginateOut)


user_schema = UsersSchema()
change_password = ChangePassword()
login_history_paginated = LoginHistoryPaginated()