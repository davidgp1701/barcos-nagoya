import io
import pandas as pd
import requests
import sheets

from datetime import date
from dateutil.relativedelta import relativedelta

sagunto_url = "https://www.valenciaportpcs.net/portcalls/Search/ExportBerths"
worksheet_title = "Puerto Sagunto"

unwanted_ships = [
    "AFRICAN WIND",
    "ATLANTIC ISLAND",
    "AMILCAR",
    "ARAMIS",
    "AYA M",
    "BARBARA P",
    "BARCELONA EXPRESS",
    "CMA CGM NEVA",
    "ECO ADRIATICA",
    "EEMS STREAM",
    "ELYSSA",
    "ERLE",
    "EUROCARGO LIVORNO",
    "EUROCARGO ROMA",
    "FRI BERGEN",
    "GAS AEGEAN",
    "GENOA EXPRESS",
    "GLEN",
    "GRANDE PORTOGALLO",
    "GULF WEST",
    "KRIENS",
    "JONA SOPHIE",
    "LADY ANNEKE",
    "LIVORNO EXPRESS",
    "LNG IMO",
    "MARANT",
    "MISSISSAUGA EXPRESS",
    "NASHWAN",
    "OLD WINE",
    "PROMISE",
    "SIKINOS",
    "SONANGOL SAMBIZANGA",
    "SPRING BREEZE",
    "STARVIP",
    "SYROS ISLAND",
    "WILSON BRUGGE",
    "ZUIDVLIET",
]


def setup():
    session = requests.Session()

    return session


def get_next_ships(session):
    print("Requesting data from Sagunto")

    request_data = {
        "IsHistoricRequest": "False",
        "PortOfValencia": "false",
        "PortOfSagunto": "true",
        "PortOfGandia": "false",
        "StatusPRV": "true",
        "StatusAUT": "true",
        "StatusOPE": "true",
        "StatusFIN": "false",
        "X-Requested-With": "hiddenIframe",
    }

    today = date.today()
    two_months = today - relativedelta(days=1) + relativedelta(months=2)

    request_data["DateFrom"] = today.strftime("%Y-%m-%d") + "T00:00:00"
    request_data["DateTo"] = two_months.strftime("%Y-%m-%d") + "T00:00:00"

    with session.post(sagunto_url, data=request_data, stream=True) as r:
        with io.BytesIO(r.content) as fh:
            df = pd.io.excel.read_excel(fh, skiprows=3)
            df = df[~df["Buque"].isin(unwanted_ships)]

            sheet = sheets.get_sheet(worksheet_title)
            sheet.df_to_sheet(df.iloc[::-1], index=0, replace=True)

    print("Got data from Sagunto")
    print()
