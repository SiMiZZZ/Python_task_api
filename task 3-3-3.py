import requests
import json
import pandas as pd
from numpy import nan
#request: https://api.hh.ru/vacancies/?specialization=1&page=1&per_page=100

page = 1
per_page = 100
vacancies_list = []
date_from = "2022-12-15T00:00:00"
date_to =  "2022-12-15T12:00:00"
for i in range(40):
    if i>=20:
        date_from = "2022-12-12T12:00:01"
        date_to = "2022-12-12T23:59:59"
        i -= 20
    link = f"https://api.hh.ru/vacancies/?specialization=1&page={i}&\
per_page=100&date_from={date_from}&date_to={date_to}"
    req = requests.get(link)
    data = req.content.decode()
    req.close()
    vacancies = json.loads(data)["items"]
    print(len(vacancies))
    for item in vacancies:
        name = item["name"]
        try:
            salary_from = item["salary"]["from"]
            salary_to = item["salary"]["to"]
            salary_currency = item["salary"]["currency"]
        except TypeError:
            salary_from = nan
            salary_to = nan
            salary_currency = nan
        area_name = item["area"]["name"]
        published_at = item["published_at"]
        vacancies_list.append([name, salary_from, salary_to, salary_currency, area_name, published_at])


vacancies_df = pd.DataFrame(vacancies_list, columns=["name", "salary_from", "salary_to", "salary_currency", "area_name", "published_at"])
vacancies_df.to_csv("vacancies_from_hh.csv", index=False)

