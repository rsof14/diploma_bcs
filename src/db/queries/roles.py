from uuid import UUID

from db.models import Roles, ObjectsPermissions, SystemObjects


def get_role_by_id(role_id: UUID):
    return Roles.query.filter_by(id=role_id).first()


def get_role_objects(role_id: UUID):
    return (ObjectsPermissions.query.join(SystemObjects, SystemObjects.object_name == ObjectsPermissions.object).
            add_columns(ObjectsPermissions.object, SystemObjects.ru_name, ObjectsPermissions.permission, SystemObjects.display_in_menu).
            filter(ObjectsPermissions.role_id == role_id, SystemObjects.display_in_menu == True).order_by(SystemObjects.ru_name).all())
