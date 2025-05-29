import os
import base64
import gspread
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

_SPREADSHEET_ID = "1-6B76PRvp6-KKl_cqj9wTt4jWO73GZ8mac_hXJdRC4c"
_spreadsheet = None

def get_spreadsheet() -> gspread.Spreadsheet:
    global _spreadsheet
    if _spreadsheet:
        return _spreadsheet

    creds_b64 = os.getenv("GOOGLE_CREDENTIALS_B64")
    if not creds_b64:
        raise RuntimeError("Missing GOOGLE_CREDENTIALS_B64")

    with open("credentials.json", "wb") as f:
        f.write(base64.b64decode(creds_b64))

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    _spreadsheet = client.open_by_key(_SPREADSHEET_ID)

    return _spreadsheet
