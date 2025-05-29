import gspread
import base64
import os
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
# Загрузка переменных окружения из .env файла
load_dotenv()

# Раскодируем base64-переменную в файл credentials.json
creds_b64 = os.environ.get("GOOGLE_CREDENTIALS_B64")
if not creds_b64:
    raise RuntimeError("Environment variable GOOGLE_CREDENTIALS_B64 not set")

with open("credentials.json", "wb") as f:
    f.write(base64.b64decode(creds_b64))

# Авторизация через gspread
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Доступ к таблице
spreadsheet = client.open_by_key("1-6B76PRvp6-KKl_cqj9wTt4jWO73GZ8mac_hXJdRC4c")
sheet = spreadsheet.worksheet("стекла")
# Получение всех строк
rows = sheet.get_all_values()

# Построение словаря
glass_prices_legal = {}
for row in rows[1:]:  # Пропускаем заголовок
    name = row[1].strip() if len(row) > 1 else None
    try:
        price = int(row[2].strip()) if row[2].strip() else 0
    except (IndexError, ValueError):
        price = 0
    if name:
        glass_prices_legal[name] = price

def get_glass_price_legal():
    """
    Получает цены на стекло из Google Sheets.
    
    Returns:
        dict: Словарь с названиями стекол и их ценами.
    """
    return glass_prices_legal

from pprint import pprint
# Для проверки
pprint(get_glass_price_legal())