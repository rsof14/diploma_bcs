import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Date, ForeignKey, String, Text, ForeignKeyConstraint, JSON, REAL
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


class Portfolio(db.Model):
    __tablename__ = 'portfolio'

    account = Column(String(8), primary_key=True, unique=True, nullable=False)
    customer_id = Column(UUID(as_uuid=True), nullable=False)
    strategy_id = Column(UUID(as_uuid=True), nullable=False)
    structure = Column(JSON)
    asset_manager = Column(UUID(as_uuid=True))
    creation_date = Column(Date, nullable=False)
    updated = Column(Boolean)

    def __init__(self, account):
        self.account = account

    def __repr__(self):
        return f'<Portfolio {self.account}>'


class Strategy(db.Model):
    __tablename__ = 'strategy'

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    name = Column(Text, nullable=False)
    currency = Column(String(3), nullable=False)
    type = Column(Text, nullable=False)
    risk_profile = Column(Text)
    structure = Column(JSON)
    valid = Column(Boolean)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Strategy {self.name}>'


class Customer(db.Model):
    __tablename__ = 'customer'

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    name = Column(Text, nullable=False)
    branch = Column(Text)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Customer {self.name}>'


class PortfolioValue(db.Model):
    __tablename__ = 'portfolio_values'

    account = Column(String(8), primary_key=True, unique=True, nullable=False)
    date = Column(Date, primary_key=True, unique=True, nullable=False)
    value = Column(REAL, nullable=False)

    def __init__(self, account, date, value):
        self.account = account
        self.date = date
        self.value = value

    def __repr__(self):
        return f'<Portfolio {self.account} value {self.value} on the {self.date}>'


class RiskProfile(db.Model):
    __tablename__ = 'risk_profile'

    name = Column(Text, primary_key=True, unique=True, nullable=False)
    max_var = Column(REAL, nullable=False)

    def __init__(self, name, max_var):
        self.name = name
        self.max_var = max_var

    def __repr__(self):
        return f'<Risk profile {self.name} max VaR {self.max_var}>'


class PortfolioRisks(db.Model):
    __tablename__ = 'portfolio_risks'

    risk_metric = Column(Text, primary_key=True, unique=True, nullable=False)
    account = Column(String(8), primary_key=True, unique=True, nullable=False)
    value = Column(REAL, nullable=False)
    updated = Column(Boolean)
    violation = Column(Boolean)

    def __init__(self, risk_metric, account, value, updated, violation):
        self.risk_metric = risk_metric
        self.account = account
        self.value = value
        self.updated = updated
        self.violation = violation

    def __repr__(self):
        return f'<Portfolio risks {self.account} metric {self.risk_metric} value {self.value}>'