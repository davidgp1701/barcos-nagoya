import gspread
from gspread_pandas import Spread


spreadsheet = "Vigilante de Sagunto"


def login():
    gc = gspread.service_account()
    sh = gc.open(spreadsheet)
    return sh


def get_worksheet(title):
    sh = login()
    worksheet = sh.worksheet(title)

    return worksheet


def get_sheet(title):
    return Spread(spread=spreadsheet, sheet=title)
