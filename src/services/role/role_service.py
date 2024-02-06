import logging

from db.queries.roles import (
    get_role_by_id
)
from uuid import UUID


def get_role_name(role_id: UUID):
    return get_role_by_id(role_id).name

