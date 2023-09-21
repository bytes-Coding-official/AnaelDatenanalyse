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

hw1 = df_d['D3'] - df_d['D10'] + df_d['D14A'] - np.maximum(df_d['D6'], df_d['D9'], df_d['D11'])



#D12B-Berechnung
# Bedingungen für HW1, HW2 und HW3
df_d['HW1'] = df_d['D3'] - df_d['D10'] + df_d['D14A'] - np.maximum(df_d['D6'], df_d['D9'], df_d['D11'])
bedingung_hw2_1 = df_c['C21'].str[18] == 'Y'
bedingung_hw2_2 = df_c['C27'].isin(['01', '90'])
df_c['HW2'] = df_c[bedingung_hw2_1 & bedingung_hw2_2]['C19'].sum()
bedingung_hw3_1 = (df_c['C21'].str[10] == 'N') & (df_c['C21'].str[18] == 'N')
bedingung_hw3_2 = df_c['C27'] == '90'
bedingung_hw3_3 = df_c['C27'] == '20'
df_c['HW3'] = df_c[(bedingung_hw3_1 & bedingung_hw3_2) | bedingung_hw3_3]['C19'].sum()

# Drei potenzielle Ergebniswerte
result_1 = df_d['HW1'] / df_d['D12A'].replace(0, np.inf)
denom_hw3 = (df_d['D6'] + df_d['D9']) / df_c['HW3'].replace(0, np.inf)
result_2 = np.where(denom_hw3 > 0, df_c['HW2'] / denom_hw3, df_c['HW2'])
result_3 = df_a['A9'] * df_c['C5'] / (df_d['D6'] + df_d['D9'] + df_d['D12A']).replace(0, np.inf)

# Die Bedingung für die Institute
institut_bedingung = df_a['A3'].isin(['10', '20']) & df_a['A8'].notna()

# Das geringste positive Ergebnis auswählen
df_d['D12B'] = np.where(
    institut_bedingung,
    np.fmin(np.fmin(result_1, result_2), result_3),
    0.00
)

# Negative Werte auf 0 setzen
df_d['D12B'] = np.where(df_d['RESULT'] < 0, 0.00, df_d['RESULT'])

#HW4-Berechnung
bedingung_hw4_1 = df_c['C21'].str[10] == 'Y'  # Position 11 ist 'Y'
bedingung_hw4_2 = df_c['C27'].isin(['01', '90'])

df_c['HW4'] = df_c[bedingung_hw4_1 & bedingung_hw4_2]['C19'].sum()

#HW5-Berechnung
# Bedingungen für HW5
bedingung_hw5_1 = (df_c['C21'].str[10] == 'N') & (df_c['C27'] == '90')
bedingung_hw5_2 = df_c['C27'] == '20'

# Summieren der kreditorischen Kontosalden basierend auf den Bedingungen
df_c['HW5'] = df_c[bedingung_hw5_1 | bedingung_hw5_2]['C19'].sum()

# Hauptbedingung für Institute
bedingung_institut = df_a['A3'].isin(['10', '20'])

# Bedingung für Feld C21
bedingung_c21 = df_c['C21'].str[10] == 'Y'

# Bedingung, dass HW1 das Produkt aus A6 und C5 übersteigt
bedingung_hw1 = df_d['HW1'] > df_a['A6'] * df_c['C5']

# Drei potenzielle Ergebniswerte
result_1 = df_d['HW1'] / (df_d['D12A'] * df_d['D12B']).replace(0, np.inf)
denom_hw5 = (df_d['D6'] + df_d['D9']) / df_c['HW5'].replace(0, np.inf)
result_2 = np.where(denom_hw5 > 0, df_c['HW4'] / denom_hw5, df_c['HW4'])
result_3 = df_a['A7'] * df_c['C5'] / (df_d['D6'] + df_d['D9'] + df_d['D12A'] + df_d['D12B']).replace(0, np.inf)

# Das geringste positive Ergebnis auswählen, wenn alle Bedingungen erfüllt sind
df_d['D12C'] = np.where(
    bedingung_institut & bedingung_c21 & bedingung_hw1,
    np.fmin(np.fmin(result_1, result_2), result_3),
    0.00
)

# Negative Werte auf 0 setzen
df_d['D12C'] = np.where(df_d['D12C'] < 0, 0.00, df_d['D12C'])
# Bedingung für Institute
bedingung_institut_d13 = df_a['A3'].isin(['01', '10'])

# Berechnung für D13
df_d['D13'] = np.where(
    bedingung_institut_d13,
    df_d['D12A'] + df_d['D12B'] + df_d['D12C'],
    0.00
)


# Bedingung für Institute
bedingung_institut_d14 = df_a['A3'].isin(['10', '20'])

# Bedingung für debitorische Kontosalden
bedingung_debitorisch = df_c['C19'] < 0

# Berechnung für D14A -> Könnte nicht ganz richtig sein...
df_d['D14A'] = np.where(
    bedingung_institut_d14,
    df_c[bedingung_debitorisch]['C19'].sum(),
    0.00
)
# Bedingung für Feld C23
bedingung_c23 = df_c['C23'].notnull() & (df_c['C23'] != '')

# Bedingung für kreditorische Kontosalden
bedingung_kreditorisch = df_c['C19'] > 0

# Berechnung für D15
df_d['D15'] = np.where(
    bedingung_c23 & bedingung_kreditorisch,
    df_c[bedingung_c23 & bedingung_kreditorisch]['C19'].sum(),
    0.00
)

print(df_a.info())
