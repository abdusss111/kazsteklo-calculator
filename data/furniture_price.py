from data.google_client import get_spreadsheet
spreadsheet = get_spreadsheet()

price_catalog_legal = {}
price_catalog_physical = {}

def parse_data(rows, price_catalog: dict):
    price_catalog.clear()
    for row in rows:
        try:
            sku = row[4].strip() if len(row) > 4 else ''
            price_str = (
                row[5].replace('\xa0', '')  # удаляем неразрывные пробелы
                .replace(',', '')   # удаляем запятые
                .strip()
                .lower()
                if len(row) > 5 else '0'
            )

            name = row[6].strip() if len(row) > 6 else ''
            price = 0 if price_str in ['x', 'х', '', '-'] else int(float(price_str))
            if sku and name:
                price_catalog[sku] = {
                    "name": name,
                    "price": price
                }
        except Exception as e:
            print(f"❌ Ошибка в строке: {row} — {e}")

def load_furniture_prices():
    rows_legal = spreadsheet.worksheet("фурнитура-юр").get_all_values()[1:]
    rows_physical = spreadsheet.worksheet("фурнитура-физ").get_all_values()[1:]
    
    parse_data(rows_legal, price_catalog_legal)
    parse_data(rows_physical, price_catalog_physical)

load_furniture_prices()

def get_furniture_price_legal():
    return price_catalog_legal

def get_furniture_price_physical():
    return price_catalog_physical
