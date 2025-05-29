from google_client import get_spreadsheet
spreadsheet = get_spreadsheet()

user_rows = spreadsheet.worksheet("пользователи").get_all_values()[1:]


def parse_users(rows) -> dict:
    users = {}
    for row in rows:
        if len(row) < 2:
            continue
        username = row[0].strip()
        password = row[1].strip()
        if username and password:
            users[username] = password
    return users