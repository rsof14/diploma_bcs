import logging

from db.queries.roles import (
    get_role_by_id,
    get_role_objects
)
from uuid import UUID


def get_role_name(role_id: UUID):
    return get_role_by_id(role_id).name


def get_role_permission_objects(role_id: UUID):
    return get_role_objects(role_id)
