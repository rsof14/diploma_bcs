from flask_migrate import Migrate

migrate = Migrate()


def init_migration_tool(app, db):
    print('migration')
    migrate.init_app(app, db=db)
