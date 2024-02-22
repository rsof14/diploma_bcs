import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import UUID

from db.pg_db import db


class Roles(db.Model):
    __tablename__ = 'roles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(200), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Role {self.name}(id: {self.id})>'


class User(db.Model):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = Column(String(200), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    password = Column(String(20), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    is_superuser = Column(Boolean, default=False)
    role_id = Column(UUID(as_uuid=True), nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(['role_id'], ['roles.id']),
    )

    def __init__(self, login, password, name, is_superuser, role_id):
        self.login = login
        self.password = password
        self.name = name
        self.is_superuser = is_superuser
        self.role_id = role_id

    def __repr__(self):
        return f'<User {self.login}>'


class LoginHistory(db.Model):
    __tablename__ = 'login_history'
    __table_args__ = (
        {
            'postgresql_partition_by': 'auth_datetime',
        }
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)
    user_agent = Column(String(250), nullable=False)
    auth_datetime = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, user_id, user_agent):
        self.user_id = user_id
        self.user_agent = user_agent

    def __repr__(self):
        return f'<LoginHistory {self.id} for user {self.user_id}>'


class SystemObjects(db.Model):
    __tablename__ = 'system_objects'

    object_name = Column(String(200), primary_key=True, unique=True, nullable=False)
    ru_name = Column(String(200), nullable=False, unique=True)
    display_in_menu = Column(Boolean)
    link = Column(Text)

    def __init__(self, name):
        self.object_name = name

    def __repr__(self):
        return f'<System object {self.object_name}>'


class ObjectsPermissions(db.Model):
    __tablename__ = 'objects_permissions'

    object = Column(String(200), primary_key=True, nullable=False)
    role_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    permission = Column(String(10), nullable=False)
    strategy_type = Column(String(80))
    id = Column(UUID(as_uuid=True))

    def __init__(self, object, role):
        self.object = object
        self.role_id = role

    def __repr__(self):
        return f'<Object permission {self.permission} for {self.object} by role {self.role_id}>'
