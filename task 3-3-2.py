import pandas as pd
from numpy import nan
from datetime import datetime
import requests

def set_salary(row, pd_currency):
    salary = 0
    if pd.isnull(row.salary_from) and pd.isnull(row.salary_to):
        return nan
    elif not pd.isnull(row.salary_from) and pd.isnull(row.salary_to):
        salary = row.salary_from
    elif pd.isnull(row.salary_from) and not pd.isnull(row.salary_to):
        salary = row.salary_to
    else:
        salary = (row.salary_from + row.salary_to)/2
    currency = row.salary_currency
    if currency not in currency_list:
        return  False
    if currency != "RUR":
        if pd.isnull(row.published_at):
            return False
        date = datetime.strptime(row.published_at, "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m")
        currency_row = pd_currency.loc[pd_currency.date == date]
        currency_to_rur = currency_row[currency].item() * salary
        return currency_to_rur
    return currency


df = pd.read_csv("vacancies_dif_currencies.csv")
parsed_df = pd.DataFrame(columns=["name", "salary", "area_name", "published_at"])
counter = 0
pd_currency = pd.read_csv('currency_rate.csv')
currency_list = list(pd_currency.columns)
for index, row in df.iterrows():
    salary = set_salary(row, pd_currency)
    if salary == False:
        continue
    new_row = {"name": row["name"], "salary": salary, "area_name": row.area_name, "published_at": row.published_at}
    parsed_df.loc[index] = pd.Series(new_row)
parsed_df.head(100).to_csv("parsed_salary.csv", index=False)
