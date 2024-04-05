from uuid import UUID

from db.models import Customer
from db.pg_db import db


def get_all_customers():
    return Customer.query.all()
