from uuid import UUID

from db.models import Roles
from db.pg_db import db


def get_all_roles():
    return Roles.query.all()


def get_one_role(role_id: UUID):
    return Roles.query.filter_by(id=role_id).first()


def does_role_exists(name: str):
    return db.session.query(Roles).filter(Roles.name == name).first()


def create_new_role(name: str):
    new_role = Roles(name=name)
    db.session.add(new_role)
    db.session.commit()


def update_role_data(role, name: str):
    role.name = name
    db.session.commit()


def delete_role_data(role):
    db.session.query(Roles).filter_by(id=role.id).delete()
    db.session.commit()