from data.google_client import get_spreadsheet
spreadsheet = get_spreadsheet()

glass_prices_legal = {}
glass_price_physical = {}
glass_prices_economy = {}

def parse_data(rows, price_catalog: dict):
    price_catalog.clear()
    for row in rows:
        name = row[1].strip() if len(row) > 1 else None
        price_str = row[2] if len(row) > 2 else ''
        price_str = price_str.replace('\xa0', '').replace(',', '').strip().lower()

        try:
            price = 0 if price_str in ['', '-', '–', 'x', 'х'] else int(float(price_str))
        except ValueError:
            price = 0

        if name:
            price_catalog[name] = price


def load_glass_prices():
    rows_legal = spreadsheet.worksheet("стекла-юр").get_all_values()
    rows_physical = spreadsheet.worksheet("стекла-физ").get_all_values()
    rows_economy = spreadsheet.worksheet("стекла-эконом").get_all_values()

    parse_data(rows_legal, glass_prices_legal)
    parse_data(rows_physical, glass_price_physical)
    parse_data(rows_economy, glass_prices_economy)

load_glass_prices()

def get_glass_price_legal():
    return glass_prices_legal

def get_glass_price_physical():
    return glass_price_physical

def get_glass_price_economy():
    return glass_prices_economy
