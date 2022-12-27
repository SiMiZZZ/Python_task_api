import pandas as pd
from datetime import datetime, date
import requests
from dateutil.relativedelta import relativedelta
import xmltodict

df = pd.read_csv("vacancies_dif_currencies.csv")

currency_counts = df.salary_currency.value_counts()
currency_list = currency_counts[lambda x: x>5000].keys().to_list()

date_frame = df.published_at[lambda x: pd.notnull(x)]

min_date = date.fromisoformat(datetime.strptime(date_frame.min(), "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d"))
max_date = date.fromisoformat(datetime.strptime(date_frame.max(), "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d"))
buf_date = min_date

currency_dict = {}
while (buf_date<max_date):
    day = str(buf_date.day) if len(str(buf_date.day)) == 2 else "0" + str(buf_date.day)
    month = str(buf_date.month) if len(str(buf_date.month)) == 2 else "0" + str(buf_date.month)
    response = requests.get(f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={day}/{month}/{buf_date.year}')
    dict_response = xmltodict.parse(response.content)['ValCurs']["Valute"]
    val_dict = {}
    for valute_dict in dict_response:
        if valute_dict['CharCode'] in currency_list:
            val_dict[valute_dict["CharCode"]] = float(valute_dict['Value'].replace(",", ".")) / int(valute_dict['Nominal'])
    currency_dict[f"{buf_date.year}-{month}"] = val_dict
    buf_date = buf_date+relativedelta(months=+1)

df = pd.DataFrame(currency_dict).T
df.to_csv("currency_rate.csv")
print(df)
print(currency_dict)