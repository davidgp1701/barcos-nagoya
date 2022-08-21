import requests
import shutil

from datetime import date
from dateutil.relativedelta import relativedelta

sagunto_url = "https://www.valenciaportpcs.net/portcalls/Search/ExportBerths"


def setup():
    session = requests.Session()

    return session


def get_next_ships(session):
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
        with open("test.xls", "wb") as f:
            shutil.copyfileobj(r.raw, f)
