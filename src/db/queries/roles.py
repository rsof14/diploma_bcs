from uuid import UUID

from db.models import Roles


def get_role_by_id(role_id: UUID):
    return Roles.query.filter_by(id=role_id).first()

