from flask import Flask, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import upgrade
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# from api.v1.admin_roles import admin_roles_bp
# from api.v1.admin_users import admin_users_bp
from api.v1.auth import auth_bp
from api.v1.models.marshmallow_init import init_marshmallow
from api.v1.users import users_bp
from core.config import app_config
from api.v1.operations import operations_bp
from api.v1.dashboard import dashboard_bp
# from core.tracing import configure_tracer
from db.alembic_migrate_init import init_migration_tool
from db.pg_db import db, init_db
from services.auth.jwt_init import init_jwt
from services.operation.operation_service import update_portfolios
from flask_apscheduler import APScheduler


def register_blueprints(app):
    API_V1_PATH = '/api/v1'
    app.register_blueprint(auth_bp, url_prefix=API_V1_PATH + '/auth')
    # app.register_blueprint(admin_roles_bp, url_prefix=API_V1_PATH + '/admin/roles')
    app.register_blueprint(users_bp, url_prefix=API_V1_PATH + '/user')
    app.register_blueprint(operations_bp, url_prefix=API_V1_PATH + '/operations')
    app.register_blueprint(dashboard_bp, url_prefix=API_V1_PATH + '/dashboard')
    # app.register_blueprint(admin_users_bp, url_prefix=API_V1_PATH + '/admin/users')


def init_extensions(app):
    init_jwt(app=app)
    init_db(app=app)
    # init_migration_tool(app=app, db=db)
    init_marshmallow(app=app)
    # limiter = Limiter(key_func=get_remote_address, storage_uri="memcached://localhost:11211")
    # limiter.init_app(app)
    FlaskInstrumentor().instrument_app(app)


# if app_config.enable_tracer:
#     configure_tracer()

scheduler = APScheduler()


def create_app():
    app = Flask(__name__)
    app.config.from_object(app_config)
    init_extensions(app)
    register_blueprints(app)
    # with app.app_context():
    #     upgrade()
    return app


def schedule_portfolios_update():
    with app.app_context():
        update_portfolios()


app = create_app()
CORS(app)
scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()
scheduler.add_job(id='update_portfolios', func=schedule_portfolios_update, trigger='cron', hour=23, minute=00)
