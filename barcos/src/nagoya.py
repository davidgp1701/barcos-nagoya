import pandas as pd
import sheets
import util
from datetime import datetime, timedelta

url = "https://www6.kaiho.mlit.go.jp/nagoyako/schedule/NAGOYAKO/schedule_3.html"
worksheet_title = "Puerto Nagoya"


def _update_date(date):
    parts = date.split("/")
    month = parts[0]
    day = parts[1]

    year = util.get_year_from_month(month)

    return "%s/%s/%s" % (year, month, day)


def _get_state(state):
    move = b"\\u79fb\\u52d5"
    entering_port = b"\\u5165\\u6e2f"
    leaving_port = b"\\u51fa\\u6e2f"

    state = state.encode("raw_unicode_escape")

    if move == state:
        return "Movimiento"
    elif entering_port == state:
        return "Entrando"
    elif leaving_port == state:
        return "Saliendo"

    return "Desconocido"


def get_forward_movements():
    ships = pd.read_html(url)
    ships = ships[0]

    # Rename columns
    ships.columns = range(ships.shape[1])

    # Drop unneeded columns
    ships = ships.drop(columns=[1, 4, 7, 8, 9, 10, 11, 12, 13])

    # Filter by the Berths we want
    ships = ships[ships[5].str.contains("I-5|I-6")]

    # Build datetime object
    ships[0] = ships[0].apply(_update_date)
    ships["Fecha"] = ships[0] + " " + ships[2]
    ships["Fecha"] = pd.to_datetime(ships["Fecha"], format="%Y/%m/%d %H:%M")
    # ships["Fecha"] = ships["Fecha"].dt.strftime("%Y/%m/%d %H:%M")
    ships = ships.drop(columns=[0, 2])

    # Convert column 3 to unicode
    ships[3] = ships[3].apply(_get_state)

    # Rename columns
    ships = ships.rename(columns={3: "Estado", 5: "Embarcadero", 6: "Nombre"})

    # Move columns
    cols = list(ships)
    # move the column to head of list using index, pop and insert
    cols.insert(0, cols.pop(cols.index("Nombre")))
    # use ix to reorder
    ships = ships.loc[:, cols]

    return ships


def get_berth_movements(movements):
    # Filter entrando
    pattern = "W[0-9]?[0-9]?(\\.[0-9][0-9]?)?→"
    to_berth = movements[movements["Embarcadero"].str.match(pattern)]
    to_berth_all = movements[movements["Nombre"].isin(to_berth["Nombre"])]
    to_berth_entrando = to_berth_all.loc[to_berth_all["Estado"] == "Entrando"]
    to_delete = to_berth[to_berth["Nombre"].isin(to_berth_entrando["Nombre"])]
    movements = (
        pd.merge(movements, to_delete, indicator=True, how="outer").query('_merge=="left_only"').drop("_merge", axis=1)
    )
    movements.loc[movements["Embarcadero"].str.match(pattern), "Estado"] = "Entrando"

    # Filter saliendo
    pattern = ".*→W[0-9]?[0-9]?(\\.[0-9][0-9]?)?"
    from_berth = movements[movements["Embarcadero"].str.match(pattern)]
    from_berth_all = movements[movements["Nombre"].isin(from_berth["Nombre"])]
    from_berth_entrando = from_berth_all.loc[from_berth_all["Estado"] == "Saliendo"]
    from_delete = from_berth[from_berth["Nombre"].isin(from_berth_entrando["Nombre"])]
    movements = (
        pd.merge(movements, from_delete, indicator=True, how="outer")
        .query('_merge=="left_only"')
        .drop("_merge", axis=1)
    )
    movements.loc[movements["Embarcadero"].str.match(pattern), "Estado"] = "Saliendo"

    return movements


def update_forward_movements():
    print("Starting to process Nagoya data")
    ships = get_forward_movements()

    sheet = sheets.get_sheet(worksheet_title)
    previous_data = sheet.sheet_to_df(index=0)
    previous_data["Fecha"] = pd.to_datetime(previous_data["Fecha"], format="%Y/%m/%d %H:%M")

    final = pd.concat([ships, previous_data]).drop_duplicates().reset_index(drop=True)
    final = final.sort_values(by=["Fecha"]).drop_duplicates(subset=["Nombre", "Estado", "Embarcadero"], keep="last")
    final = final.drop(final[final["Fecha"] < datetime.now() - timedelta(days=60)].index)

    final = get_berth_movements(final)
    final.sort_values(by=["Fecha", "Nombre"])

    sheet = sheet.df_to_sheet(final, index=0, replace=True)
    print("Processed Nagoya data")
    print()
