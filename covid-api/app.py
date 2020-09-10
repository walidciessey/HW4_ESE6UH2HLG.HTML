from flask import Flask, jsonify
from flask_cors import CORS
import requests
import csv
from io import StringIO
import datetime

app = Flask(__name__)
CORS(app)

url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"
countries = [
    "Benin",
    "Burkina Faso",
    "Cape Verde",
    "The Gambia",
    "Ghana",
    "Guinea",
    "Guinea-Bissau",
    "Ivory Coast",
    "Liberia",
    "Mali",
    "Mauritania",
    "Niger",
    "Nigeria",
    "Senegal",
    "Sierra Leone",
    "Togo",
]


def get_csv_data(url, date):
    resp = requests.get(url + date + ".csv")
    data = resp.content.decode("ascii", "ignore")
    csv_data = StringIO(data)

    return csv_data


def get_covid_cases(url, countries, date):
    csv_data = get_csv_data(url, date)
    reader = csv.reader(csv_data)
    covid_cases = []

    for row in reader:
        if row[0] == "FIPS":
            continue
        if row[3] in countries:
            covid_cases.append(
                {
                    "Country": row[3],
                    "Confirmed": row[7],
                    "Deaths": row[8],
                    "Recoveries": row[9],
                    "Active": row[10],
                }
            )
    return covid_cases


@app.route("/api/")
@app.route("/api/<date>")
def cases(date=None):
    today = datetime.datetime.today()
    yesterday = today - datetime.timedelta(days=1)

    if date is None:
        date = yesterday.strftime("%m-%d-%Y")

    covid_cases = get_covid_cases(url, countries, date)
    return jsonify({"Covid 19 Cases": covid_cases})


if __name__ == "__main__":
    app.run(port=8000, debug=True)
