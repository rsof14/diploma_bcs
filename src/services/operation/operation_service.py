from db.queries.portfolio import get_portfolios_by_user
from services.user.user_service import user_get_data


def get_portfolio_list(login: str):
    user_id = user_get_data(login).id
    return get_portfolios_by_user(user_id)
