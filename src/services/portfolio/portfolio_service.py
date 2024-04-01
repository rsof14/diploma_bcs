from db.queries.portfolio import get_all_portfolios_info


def get_info():
    return get_all_portfolios_info()


def update_portfolios_risks(portfolios_ids: dict):
    for portfolio in portfolios_ids['portfolios']:
        pass
