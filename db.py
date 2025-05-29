import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Авторизация
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Открытие таблицы
spreadsheet = client.open_by_key("1-6B76PRvp6-KKl_cqj9wTt4jWO73GZ8mac_hXJdRC4c")  # Замените на ваш ID
sheet = spreadsheet.worksheet("стекла")  # Замените на ваш лист

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