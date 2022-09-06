import pandas as pd
import requests
import sheets
from io import StringIO

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
        ]
    )

    return df


def update_forward_movements():
    print("Starting to process Portbury data")
    ships = get_forward_movements()

    sheet = sheets.get_sheet(worksheet_title)
    sheet = sheet.df_to_sheet(ships, index=0, replace=True)
    print("Processed Portbury data")
    print()
