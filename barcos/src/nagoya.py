import pandas as pd
import util

url = "https://www6.kaiho.mlit.go.jp/nagoyako/schedule/NAGOYAKO/schedule_3.html"


def update_date(date):
    parts = date.split("/")
    month = parts[0]
    day = parts[1]

    year = util.get_year_from_month(month)

    return "%s/%s/%s" % (year, month, day)


def get_forward_movements():
    ships = pd.read_html(url)
    ships = ships[0]

    # Rename columns
    ships.columns = range(ships.shape[1])

    # Drop unneeded columns
    ships = ships.drop(columns=[1, 3, 4, 7, 8, 9, 10, 11, 12, 13])

    # Filter by the Berths we want
    ships = ships[ships[5].str.contains("I-5|I-6")]

    # Build datetime object
    ships[0] = ships[0].apply(update_date)
    ships["Fecha"] = ships[0] + " " + ships[2]
    ships["Fecha"] = pd.to_datetime(ships["Fecha"], format="%Y/%m/%d %H:%M")
    ships = ships.drop(columns=[0, 2])

    # Rename columns
    ships = ships.rename(columns={5: "Embarcadero", 6: "Nombre"})

    return ships
