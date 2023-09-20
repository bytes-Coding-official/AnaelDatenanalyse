import pandas as pd
import numpy as np
#wir haben eine datei A.csv, B.csv, C.csv importiere diese mit pandas die erste zeile ist jeweils der header
#A1,A2,A3,A4,A5,A6A,A6B,A6C,A7,A8,A9A,A9B,A9C,A10
#B1,B2,B3,B4,B5,B6,B7,B8,B9,B10,B11,B12,B13,B14,B15,B16
#C1,C2A,C2B,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,C13,C14,C15,C16,C17,C18,C19,C20,C21,C22,C23,C24,C25,C26,C27

df_a = pd.read_csv('A.csv', sep=',', header=0)
df_b = pd.read_csv('B.csv', sep=',', header=0)
df_c = pd.read_csv('C.csv', sep=',', header=0)
df_d = pd.read_csv('D.csv', sep=',', header=0)
df_e = pd.read_csv('E.csv', sep=',', header=0)

#in spalte D1 in D muss immer die Konstante "D" stehen
df_d['D1'] = 'D'

#Bei D2 ist es der Wert aus B2
df_d['D2'] = df_b['B2']

#Der Wert in D3 ist es der Wert aus C19 (reihe pro reihe)
df_d['D3'] = df_c['C19']

#D4 =

# Bedingung 1
bedingung_a = df_a['A3'].isin(['01', '10'])

# Bedingung für B14
bedingung_b = df_b['B14'].str.slice(0, 30).str.contains('Y', na=False)

# Bedingungen für C19 und C20
bedingung_c1 = df_c['C19'] > 0  # kreditorischer Kontosaldo
bedingung_c2 = df_c['C20'].str[0] == 'Y'   # Wert "Y" an Position "01" in C20
bedingung_c3 = df_c['C20'].str.slice(1, 30).str.contains('Y', na=False)  # Wert "Y" zwischen Positionen "02" bis "30" in C20
# Bedingung für D3
bedingung_d = df_d['D3'] < 20

# Ergebnisse berechnen 
df_d['D4'] = np.where(
    bedingung_a & bedingung_b,
    df_c['C19'],
    np.where(
        bedingung_a & bedingung_d & bedingung_c2,
        df_d['D3'],
        np.where(
            bedingung_a & bedingung_c3,
            df_c['C19'],
            0.00
        )
    )
)

bedingung_a = df_a['A3'].isin(['01', '10'])

# Ergebnis für D5 basierend auf der Bedingung berechnen
df_d['D5'] = np.where(
    bedingung_a,
    df_d['D3'] - df_d['D4'],
    0.00
)

bedingung_a = df_a['A3'].isin(['01', '10'])

# Berechnung des maximalen Wertes für D6
max_wert = df_a['A4'] * df_c['C5']

# Ergebnis für D6 basierend auf der Bedingung berechnen
df_d['D6'] = np.where(
    bedingung_a,
    np.minimum(df_d['D5'], max_wert),
    0.00
)
# Bedingung für Institute mit Wert "01" oder "10" in Feld A3
bedingung_a = df_a['A3'].isin(['01', '10'])

# Ergebnis für D7 basierend auf der Bedingung berechnen
df_d['D7'] = np.where(
    bedingung_a,
    df_d['D5'] - df_d['D6'],
    0.00
)

# D8-Berechnung
bedingung_c8 = df_c['C22'].notnull() & (df_c['C19'] > 0) & (df_c['C22'] != "DE")
df_d['D8'] = df_c[bedingung_c8]['C19'].sum()


# D9-Berechnung
bedingung_a9 = df_a['A3'] == '20'
max_wert_d9 = df_a['A5'] * df_c['C5']

df_d['D9'] = np.where(
    bedingung_a9,
    np.minimum(df_d['D3'], max_wert_d9),
    0.00
)


# D10-Berechnung
bedingung_a10 = df_a['A3'].isin(['10', '20'])
bedingung_c10 = df_c['C27'] == '10'

df_d['D10'] = np.where(
    bedingung_a10,
    df_c[bedingung_c10 & (df_c['C19'] > 0)]['C19'].sum(),
    0.00
)

# D11-Berechnung
bedingung_c11 = df_c['C27'] == '20'

df_d['D11'] = np.where(
    bedingung_a10,
    df_c[bedingung_c11 & (df_c['C19'] > 0)]['C19'].sum() - df_c[bedingung_c11]['C26'].sum(),
    0.00
)

# HW1-Berechnung als Platzhalter
hw1 = df_d['D3'] - df_d['D10'] + df_d['D14A'] - np.maximum(df_d['D6'], df_d['D9'], df_d['D11'])

# D12A-Berechnung
max_wert_d12a = (df_a['A6'] * df_c['C5']) - (df_d['D6'] + df_d['D9'])

bedingung_a12a = df_a['A3'].isin(['10', '20'])
df_d['D12A'] = np.where(
    bedingung_a12a & (hw1 <= max_wert_d12a) & (hw1 > 0),
    hw1,
    0.00
)

#NICHT VEKTORWEISE SONDERN ZEILENWEISE
def calculate_d12a(row):
    hw1 = row['D3'] - row['D10'] + row['D14A'] - max(row['D6'], row['D9'], row['D11'])
    max_wert_d12a = row['A6'] * row['C5'] - (row['D6'] + row['D9'])

    if row['A3'] in ['10', '20'] and hw1 <= max_wert_d12a and hw1 > 0:
        return hw1
    else:
        return 0.00

df_d['D12A'] = df.apply(calculate_d12a, axis=1)

print(df_a.info())
