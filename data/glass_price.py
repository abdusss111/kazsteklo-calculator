import gspread
import base64
import os
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()

creds_b64 = os.environ.get("GOOGLE_CREDENTIALS_B64")
if not creds_b64:
    raise RuntimeError("Environment variable GOOGLE_CREDENTIALS_B64 not set")

with open("credentials.json", "wb") as f:
    f.write(base64.b64decode(creds_b64))

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
spreadsheet = client.open_by_key("1-6B76PRvp6-KKl_cqj9wTt4jWO73GZ8mac_hXJdRC4c")

glass_prices_legal = {}
glass_price_physical = {}
glass_prices_economy = {}

def parse_data(rows, price_catalog: dict):
    price_catalog.clear()
    for row in rows:
        name = row[1].strip() if len(row) > 1 else None
        try:
            price = int(row[2].strip()) if len(row) > 2 and row[2].strip() else 0
        except (IndexError, ValueError):
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
