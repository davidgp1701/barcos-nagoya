import pandas as pd

url = "https://www6.kaiho.mlit.go.jp/nagoyako/schedule/NAGOYAKO/schedule_3.html"


def get_forward_movements():
    ships = pd.read_html(url)[0]
    ships.columns = range(ships[1])

    return ships[ships[5].str.contains("I-5|I-6")]
