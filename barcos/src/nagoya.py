import pandas as pd

url = "https://www6.kaiho.mlit.go.jp/nagoyako/schedule/NAGOYAKO/schedule_3.html"


def get_forward_movements():
    list_of_df = pd.read_html(url)
    print(len(list_of_df))
