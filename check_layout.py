import pandas as pd

xls = pd.ExcelFile("data/Brigade Road - Store layoutc5f5d56.xlsx")

print("Sheets:")
print(xls.sheet_names)

df = pd.read_excel(
    "data/Brigade Road - Store layoutc5f5d56.xlsx"
)

print("\nFirst 5 rows:")
print(df.head())

print("\nColumns:")
print(df.columns.tolist())