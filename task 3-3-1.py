import pandas as pd

df = pd.read_csv("vacancies_dif_currencies.csv")

print(df.salary_currency.value_counts())
