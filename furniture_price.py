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

# Открываем нужный лист
sheet = client.open_by_key("1-6B76PRvp6-KKl_cqj9wTt4jWO73GZ8mac_hXJdRC4c").worksheet("фурнитура")  # замените на ваш лист

rows = sheet.get_all_values()[1:]  

price_catalog_legal = {}

for row in rows:
    try:
        sku = row[4].strip()  # E-столбец
        price_str = row[5].replace(',', '').strip() if len(row) > 5 else '0'
        if price_str in ['x', 'х', '', '-']:
            price = 0
        price = int(float(price_str)) if price_str and price_str != "х" else 0
        name = row[6].strip() if len(row) > 6 else ''
        
        if sku and name:
            price_catalog_legal[sku] = {
                "name": name,
                "price": price
            }
    except Exception as e:
        print(f"❌ Ошибка в строке: {row} — {e}")

# ✅ Проверка
from pprint import pprint
pprint(price_catalog_legal)
