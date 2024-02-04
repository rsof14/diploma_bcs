import logging

from db.queries.roles import (
    get_all_roles,
    does_role_exists,
    create_new_role,
    get_one_role,
    update_role_data,
    delete_role_data
)
from uuid import UUID


class RoleAlreadyExists(Exception):
    ...


class RoleNotFound(Exception):
    ...


def roles_get_data():
    return get_all_roles()


def create_role(name: str):
    if does_role_exists(name):
        logging.warning('Role %s already exists in db', name)
        raise RoleAlreadyExists('Role already exist')

    create_new_role(name)
    logging.info('Role %s created successfully in db', name)


def get_role_data(role_id: UUID):
    role = get_one_role(role_id)
    if not role:
        logging.warning('Role %s not found in db', role_id)
        raise RoleNotFound('Role not found in db')

    return role


def get_role_by_name(name: str):
    role = does_role_exists(name)
    if not role:
        raise RoleNotFound('Role %s not found in db', name)

    return role


def update_role(role_id: UUID, name: str):
    try:
        role = get_role_data(role_id)
    except RoleNotFound:
        raise
    if does_role_exists(name):
        raise RoleAlreadyExists('Role with this name already exist in db')

    update_role_data(role, name)
    logging.info('Role in db %s updated successfully', name)


def delete_role(role_id: UUID):
    role = get_role_data(role_id)
    delete_role_data(role)
    logging.info('Role in db %s deleted successfully', role_id)