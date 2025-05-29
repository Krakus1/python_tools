import pandas as pd

# # Podaj ścieżkę do pliku CSV
# csv_file = 'Historia_transakcji_test.csv'

# # Wczytaj zawartość pliku CSV do DataFrame
# df = pd.read_csv(csv_file)

# # Wyświetl pierwsze 5 wierszy DataFrame
# # print(df.head())

# # Przykład ścieżki do pliku na OneDrive (lokalna synchronizacja)
# onedrive_path = r'C:\Users\vbaAp\OneDrive\Documents\Fin\mill_transaction.csv'
# df_onedrive = pd.read_csv(onedrive_path)
# # print(df_onedrive.head())

# # print (df.columns)

# # # Wyświetl tylko wybrane kolumny, np. 'Data' i 'Kwota'
# selected_columns = ['Data transakcji','Opis', 'Obciążenia']
# # print(df[selected_columns])

# # # Wypisz unikalne wartości z wybranej kolumny, np. 'Opis'
# # unique_values = df['Rodzaj transakcji'].unique()
# # print(unique_values)

# # Przefiltruj wiersze, gdzie kolumna 'Obciążenia' nie jest pusta
# filtered_df = df[df['Obciążenia'].notna() & (df['Obciążenia'] != '')]

# # Wczytaj słownik wykluczonych opisów
# excluded_dict_path = r'C:\Users\vbaAp\OneDrive\Documents\Fin\trans_excluded.csv'
# try:
#     excluded_df = pd.read_csv(excluded_dict_path)
#     excluded_descriptions = excluded_df['Opis'].unique()
# except FileNotFoundError:
#     excluded_descriptions = []

# # Przefiltruj, aby pozostały tylko rekordy, których opis NIE znajduje się w słowniku wykluczonych
# filtered_df = filtered_df[~filtered_df['Opis'].isin(excluded_descriptions)]
# # print(filtered_df[selected_columns])
# # Przemnóż wartości w kolumnie 'Obciążenia' przez -1
# filtered_df['Obciążenia'] = filtered_df['Obciążenia'].astype(float) * -1
# # print(filtered_df[selected_columns])

# filtered_to_append = filtered_df.rename(columns={
#     'Data transakcji': 'Data',
#     'Opis': 'Opis',
#     'Obciążenia': 'Kwota'
# })[['Data', 'Opis', 'Kwota']]

# # Usuń wiersze, które już istnieją w df_onedrive (po Data, Opis, Kwota)
# merged = pd.merge(
#     filtered_to_append,
#     df_onedrive[['Data','Kwota']],
#     on=['Data','Kwota'],
#     how='left',
#     indicator=True
# )

# #print (merged)
# merged = merged.sort_values(by='Data', ascending=True)

# to_add = merged[merged['_merge'] == 'left_only'].drop(columns=['_merge'])

# # Wyznacz nowe ID
# if 'ID' in df_onedrive.columns:
#     max_id = df_onedrive['ID'].max()
#     if pd.isna(max_id):
#         max_id = 0
# else:
#     max_id = 0
#     df_onedrive['ID'] = []

# new_ids = range(int(max_id) + 1, int(max_id) + 1 + len(to_add))
# to_add.insert(0, 'ID', new_ids)

# # Wyznacz nowy okres
# if 'Okres' in df_onedrive.columns:
#     max_okres = df_onedrive['Okres'].max()
#     if pd.isna(max_okres):
#         max_okres = 0
# else:
#     max_okres = 0
#     df_onedrive['Okres'] = []

# new_okres = int(max_okres) + 1
# to_add['Okres'] = new_okres

# # Wyświetl użytkownikowi rekordy do dodania
# print("Rekordy do dodania:")
# print(to_add)

# # Pozwól użytkownikowi wskazać numery ID (z kolumny 'ID' w to_add), które mają nie być dodane
# exclude_input = input("Podaj numery ID (oddzielone przecinkami), które mają NIE być dodane (lub Enter, aby dodać wszystkie): ")
# exclude_ids = []
# if exclude_input.strip():
#     exclude_ids = [int(x.strip()) for x in exclude_input.split(',') if x.strip().isdigit()]

# # Rekordy do wykluczenia
# excluded_records = to_add[to_add['ID'].isin(exclude_ids)]
# to_add = to_add[~to_add['ID'].isin(exclude_ids)]

# # Dodaj opisy wykluczonych rekordów do słownika wykluczeń
# if not excluded_records.empty:
#     excluded_descriptions = excluded_records['Opis'].unique()
#     excluded_dict_path = r'C:\Users\vbaAp\OneDrive\Documents\Fin\trans_excluded.csv'
#     try:
#         excluded_df = pd.read_csv(excluded_dict_path)
#     except FileNotFoundError:
#         excluded_df = pd.DataFrame(columns=['Opis'])

#     # Dodaj nowe opisy, unikając duplikatów
#     new_excluded = pd.DataFrame({'Opis': excluded_descriptions})
#     excluded_df = pd.concat([excluded_df, new_excluded], ignore_index=True).drop_duplicates(subset=['Opis'])

#     excluded_df.to_csv(excluded_dict_path, index=False)


# df_onedrive_updated = pd.concat([df_onedrive, to_add], ignore_index=True)

# # Zapisz wynik (opcjonalnie)
# df_onedrive_updated.to_csv(onedrive_path, index=False)

# print('Dane zostały zaktualizowane i zapisane w pliku:', onedrive_path)
# # ...existing code...

# Ścieżki do plików``
TRANS_FILE = 'Historia_transakcji_20250529_122255.csv'
ONEDRIVE_PATH = r'C:\Users\vbaAp\OneDrive\Documents\Fin\mill_transaction.csv'
EXCLUDED_DICT_PATH = r'C:\Users\vbaAp\OneDrive\Documents\Fin\trans_excluded.csv'

def load_excluded_descriptions(path):
    try:
        df = pd.read_csv(path)
        return df['Opis'].unique()
    except FileNotFoundError:
        return []

def update_excluded_descriptions(path, new_descriptions):
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Opis'])
    new_df = pd.DataFrame({'Opis': new_descriptions})
    df = pd.concat([df, new_df], ignore_index=True).drop_duplicates(subset=['Opis'])
    df.to_csv(path, index=False)

# Wczytaj dane
df = pd.read_csv(TRANS_FILE)
df_onedrive = pd.read_csv(ONEDRIVE_PATH)

# Filtrowanie i przygotowanie danych
selected_columns = ['Data transakcji', 'Opis', 'Obciążenia']
filtered_df = df[df['Obciążenia'].notna() & (df['Obciążenia'] != '')].copy()

excluded_descriptions = load_excluded_descriptions(EXCLUDED_DICT_PATH)
filtered_df = filtered_df[~filtered_df['Opis'].isin(excluded_descriptions)].copy()

filtered_df.loc[:, 'Obciążenia'] = filtered_df['Obciążenia'].astype(float) * -1

filtered_to_append = filtered_df.rename(columns={
    'Data transakcji': 'Data',
    'Opis': 'Opis',
    'Obciążenia': 'Kwota'
})[['Data', 'Opis', 'Kwota']]

# Usuń wiersze już istniejące
merged = pd.merge(
    filtered_to_append,
    df_onedrive[['Data', 'Kwota']],
    on=['Data', 'Kwota'],
    how='left',
    indicator=True
)
merged = merged.sort_values(by='Data', ascending=True)
to_add = merged[merged['_merge'] == 'left_only'].drop(columns=['_merge'])

# Nowe ID
if 'ID' in df_onedrive.columns:
    max_id = df_onedrive['ID'].max()
    if pd.isna(max_id):
        max_id = 0
else:
    max_id = 0
    df_onedrive['ID'] = []

new_ids = range(int(max_id) + 1, int(max_id) + 1 + len(to_add))
to_add.insert(0, 'ID', new_ids)

# Nowy okres
if 'Okres' in df_onedrive.columns:
    max_okres = df_onedrive['Okres'].max()
    if pd.isna(max_okres):
        max_okres = 0
else:
    max_okres = 0
    df_onedrive['Okres'] = []

new_okres = int(max_okres) + 1
to_add['Okres'] = new_okres

# Wyświetl rekordy do dodania
print("Rekordy do dodania:")
print(to_add)

# Pozwól użytkownikowi wykluczyć ID
exclude_input = input("Podaj numery ID (oddzielone przecinkami), które mają NIE być dodane (lub Enter, aby dodać wszystkie): ")
exclude_ids = []
if exclude_input.strip():
    exclude_ids = [int(x.strip()) for x in exclude_input.split(',') if x.strip().isdigit()]

excluded_records = to_add[to_add['ID'].isin(exclude_ids)]
to_add = to_add[~to_add['ID'].isin(exclude_ids)]

# Aktualizuj słownik wykluczeń
if not excluded_records.empty:
    update_excluded_descriptions(EXCLUDED_DICT_PATH, excluded_records['Opis'].unique())

# Zaktualizuj i zapisz plik
df_onedrive_updated = pd.concat([df_onedrive, to_add], ignore_index=True)
df_onedrive_updated.to_csv(ONEDRIVE_PATH, index=False)

print('Dane zostały zaktualizowane i zapisane w pliku:', ONEDRIVE_PATH)