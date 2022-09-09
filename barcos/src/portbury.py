import pandas as pd
import requests
import sheets
from io import StringIO
from gspread_formatting import cellFormat, format_cell_range, textFormat, set_column_width

url = "https://www.bristolport.co.uk/export-table/45/ForwardMovements"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
}

worksheet_title = "Puerto Portbury"

wanted_ports = ["", "LIVORNO", "SAGUNTO"]
wanted_docks = ["Portbury"]
unwanted_agents = ["TU", "KESTREL", "MED"]


def get_forward_movements():
    req = requests.get(url, headers=headers)
    data = StringIO(req.text)

    df = pd.read_csv(data)
    df = df.drop(
        columns=[
            "Rotn",
            "Cargo",
            "D - PO",
            "PL",
            "dD",
            "dpo_sort",
            "D_Tugs",
            "Comments",
            "Purpose",
            "L x B",
            "A_Tugs",
            "A - PO",
            "apo_sort",
            "ETD",
            "etd_sort",
        ]
    )

    df = df.replace(r"^\s*$", "", regex=True)
    df = df[df["From"].isin(wanted_ports)]
    df = df[df["Dock"].isin(wanted_docks)]
    df = df[~df["Agent"].isin(unwanted_agents)]

    return df


def update_forward_movements():
    print("Starting to process Portbury data")
    ships = get_forward_movements()

    sheet = sheets.get_sheet(worksheet_title)
    sheet.df_to_sheet(ships, index=0, replace=True)

    format_cells()

    print("Processed Portbury data")
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
    set_column_width(worksheet, "B", 90)
    set_column_width(worksheet, "C", 130)
    set_column_width(worksheet, "D", 100)
    set_column_width(worksheet, "E", 60)
    set_column_width(worksheet, "F", 90)
    set_column_width(worksheet, "G", 100)
    set_column_width(worksheet, "H", 40)
    set_column_width(worksheet, "I", 100)
    set_column_width(worksheet, "J", 100)
