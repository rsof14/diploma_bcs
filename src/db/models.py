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
