import io
import pandas as pd
import requests
import sheets

from datetime import date
from dateutil.relativedelta import relativedelta
from gspread_formatting import cellFormat, format_cell_range, textFormat, set_column_width

sagunto_url = "https://www.valenciaportpcs.net/portcalls/Search/ExportBerths"
worksheet_title = "Puerto Sagunto"

unwanted_terminals = ["PLANTA REGASIFICACION SGTO S.A"]

unwanted_consignatario = ["MARITIMA DEL MEDITERRANEO,S.A.", "MILLER Y CIA,S.A.", "SIMON MONTOLIO Y CIA.,S.A."]

unwanted_ships = [
    "ABERDEEN",
    "AFRICAN WIND",
    "AMBER SKY",
    "ARTABRO",
    "ATLANTIC ISLAND",
    "ATLANTIC HORIZON",
    "AMILCAR",
    "ARAMIS",
    "ASLI ELIF",
    "AYA M",
    "BARBARA P",
    "BARCELONA EXPRESS",
    "BRENS",
    "CALA PALMA",
    "CELTIC AMBASSADOR",
    "CIUDAD DE BARCELONA",
    "CIVARINA",
    "CL ZHUANG HE",
    "CMA CGM NEVA",
    "DETROIT EXPRESS",
    "ECO ADRIATICA",
    "ECO MEDITERRANEA",
    "EEMS STREAM",
    "ELYSSA",
    "ERLE",
    "EUROCARGO LIVORNO",
    "EUROCARGO ROMA",
    "FRI BERGEN",
    "FONNLAND",
    "GAS AEGEAN",
    "GAS VENUS",
    "GASLOG  SANTIAGO",
    "GENOA EXPRESS",
    "GLEN",
    "GRANDE PORTOGALLO",
    "GULF WEST",
    "HERMANA",
    "JIAN GUO HAI",
    "KOSMAN",
    "KRIENS",
    "JONA SOPHIE",
    "LADY AMALIA",
    "LADY ANNEKE",
    "LADY ANNE BEAU",
    "LADY DEBORA",
    "LIVERPOOL EXPRESS",
    "LIVORNO EXPRESS",
    "LNG IMO",
    "LNG BENUE",
    "MARANT",
    "MARIA H",
    "MARYCAM SWAN",
    "MEHMET DADAYLI-1",
    "MERI",
    "MISSISSAUGA EXPRESS",
    "MOSELDIJK",
    "NASHWAN",
    "NORD MONTREAL",
    "NORMA",
    "OLD WINE",
    "OMER DADAYLI",
    "RHODANUS",
    "PLATON",
    "PROMISE",
    "RUDOLF",
    "SAFIYE ANA",
    "SCHELDEDIJK",
    "SEAPEAK CATALUNYA",
    "SEAPEAK POLAR",
    "SIKINOS",
    "SMALAND",
    "SONANGOL SAMBIZANGA",
    "SPRING BREEZE",
    "STARVIP",
    "SYROS ISLAND",
    "ULTRA SILVA",
    "TEJO BELEM",
    "THOMAS",
    "TOP GRACE",
    "TRIPLE S",
    "WILSON BREMEN",
    "WILSON BRUGGE",
    "WILSON HAWK",
    "WILSON FARSUND",
    "WILSON HERON",
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
            df = df[~df["Terminal"].isin(unwanted_terminals)]
            df = df[~df["Consignatario buque"].isin(unwanted_consignatario)]
            df = df.drop(columns=["UN/LOCODE", "Puerto de escala"])

            sheet = sheets.get_sheet(worksheet_title)
            sheet.df_to_sheet(df.iloc[::-1], index=0, replace=True)

    format_cells()

    print("Got data from Sagunto")
    print()


def format_cells():
    worksheet = sheets.get_worksheet(worksheet_title)

    fmt_header = cellFormat(
        textFormat=textFormat(bold=True),
    )
    format_cell_range(worksheet, "1", fmt_header)

    fmt_normal = cellFormat(textFormat=textFormat(bold=False))
    format_cell_range(worksheet, "2:1000", fmt_normal)

    set_column_width(worksheet, "A", 160)
    set_column_width(worksheet, "B", 85)
    set_column_width(worksheet, "C", 70)
    set_column_width(worksheet, "D", 130)
    set_column_width(worksheet, "E", 130)
    set_column_width(worksheet, "F", 200)
    set_column_width(worksheet, "G", 200)
    set_column_width(worksheet, "H", 200)
