import logging

from flask_sqlalchemy.pagination import Pagination

from db.queries.user import (
    get_user_by_login,
    get_login_history,
    does_user_exist,
    user_admin_all,
    get_user_by_id
)
from db.pg_db import db
from services.role.role_service import get_role_by_name, RoleNotFound
from uuid import UUID
from sqlalchemy.exc import DataError


class LoginAlreadyExists(Exception):
    ...


class UserNotFound(Exception):
    ...


def user_get_data(login: str):
    return get_user_by_login(login)


def user_login_history(login: str, page: int, page_size: int):
    user_id = get_user_by_login(login).id
    history = get_login_history(user_id, page, page_size)
    return get_paginated(history)


def get_paginated(paginated_obj: Pagination):
    return {
        'results': paginated_obj.items,
        'pagination': {
            'page': paginated_obj.page,
            'per_page': paginated_obj.per_page,
            'pages_total': paginated_obj.pages
        }
    }


def get_user_admin_info():
    return user_admin_all()


def get_user_info(user_id: UUID):
    user = get_user_by_id(user_id)
    if not user:
        raise UserNotFound('User not found')
    logging.info('User in db %s found', user_id)

    return user
