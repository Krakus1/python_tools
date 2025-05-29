import pandas as pd

# Wczytaj plik Excela (podaj właściwą ścieżkę do pliku)
EXCEL_PATH = './test.xlsx'

# Wczytaj tabelę o nazwie "tab_test"
data_1 = pd.read_excel(EXCEL_PATH, sheet_name='Sheet1')
data_2 = pd.read_excel(EXCEL_PATH, sheet_name='Sheet2')
# Wczytaj dane z pierwszego arkusza

result_1 = []
for idx, row in data_1.iterrows():
    value = row.iloc[0]
    x_2 = str(value)[0] if len(str(value)) > 0 else ''
    x_1 = float(str(value)[1:] if len(str(value)) > 1 else '')
    for col_name in data_1.columns[1:]:
        x_3 = col_name
        x_4 = row[col_name]
        result_row_1 = [x_2, x_1, x_3, x_4]
        # Zbierz dane do listy
        result_1.append(result_row_1)

result_2 = []
for idx, row in data_2.iloc[1:].iterrows():  # zaczynamy od drugiego wiersza (pomijamy nagłówek)
    x_1 = float(row.iloc[0])  # pierwsza kolumna to x_1
    for col_idx, col_name in enumerate(data_2.columns[1:], start=1):  # od drugiej kolumny
        # Rozdziel nagłówek na x_3 i x_2
        if '_' in col_name:
            x_3, x_2 = col_name.split('_', 1)
        else:
            x_3, x_2 = col_name, ''
        x_5 = float(row.iloc[col_idx])  # wartość w danej komórce
        result_row_2 = [x_2, x_1, x_3, x_5]
        # Zbierz dane do listy
        result_2.append(result_row_2)

df_1 = pd.DataFrame(result_1, columns=['x2', 'x1', 'x3', 'x4'])
df_2 = pd.DataFrame(result_2, columns=['x2', 'x1', 'x3', 'x5'])

merged = pd.merge(df_1, df_2, on=['x1', 'x2', 'x3'], how='left')

print(merged)
