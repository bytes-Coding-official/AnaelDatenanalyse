import pandas
import numpy as np


dataframe_a = pandas.read_csv('../files/A.csv', sep=',', header=0)
dataframe_b = pandas.read_csv('B.csv', sep=',', header=0)
dataframe_c = pandas.read_csv('C.csv', sep=',', header=0)
dataframe_d = pandas.read_csv('D.csv', sep=',', header=0)
dataframe_e = pandas.read_csv('E.csv', sep=',', header=0)
dataframe_a_b_c = pandas.read_csv('A_B_C.csv', sep=',', header=0)

def set_C27_value(row):
    # Wert: 90 - Ohne Ausschluss
    if all(row['B14'] == 'N') and all(row['C20'] == 'N'):
        return '90'

    # Wert: 01 - Ausschluss nur nach EinSiG
    if any(row['B14'][0:15] == 'Y') and all(row['B14'][15:50] == 'N') and all(row['C20'][10:50] == 'N'):
        return '01'
    elif any(row['C20'][0:10] == 'Y') and all(row['C20'][10:50] == 'N') and all(row['B14'][15:50] == 'N'):
        return '01'

    # Wert: 20 - Ausschluss nur nach ESF-Statut
    if any(row['B14'][30:50] == 'Y') and all(row['B14'][0:30] == 'N') and all(row['C20'][0:30] == 'N'):
        return '20'
    elif any(row['C20'][30:50] == 'Y') and all(row['C20'][0:30] == 'N') and all(row['B14'][0:30] == 'N'):
        return '20'

    # Wert: 11 - Ausschluss "Bagatellgrenze" nach EinSiG und ESF-Statut
    if all(row['C20'][1:49] == 'N') and row['C20'][49] == 'Y':
        return '11'

    # Wert: 10 - Ausschluss nach EinSiG und ESF-Statut (alle anderen Fälle)
    return '10'

# Anwenden der Funktion auf den DataFrame
dataframe_c['C27'] = dataframe_c.apply(set_C27_value, axis=1)


# drop all values from dataframe_d
#dataframe_d = dataframe_d.iloc[0:0]
# kundennummer bei B2 und C2A verbinde dort nicht alle C2A sind in B2 enthalten
dataframe_b['B2'] = dataframe_b['B2'].astype(str)
dataframe_c['C2A'] = dataframe_c['C2A'].astype(str)
dataframe_d['D1'] = 'D'
dataframe_b["B1"] = "B"
dataframe_c["C1"] = "C"

def generate_random_data():
    global dataframe_b
    global dataframe_c
    dataframe_b = pandas.DataFrame(np.random.randint(0, 75, size=(100, 16)), columns=dataframe_b.columns)

    # Setting the first 20 values in column B2 to range from 0 to 19
    dataframe_b.loc[:19, "B2"] = np.arange(20)
    dataframe_c = pandas.DataFrame(np.random.randint(0, 200, size=(150, 28)), columns=dataframe_c.columns)

    global dataframe_b_c
    # verbinde die den dataframe B und C anhand der werte aus B2 und C2A
    dataframe_b_c = pandas.merge(dataframe_b, dataframe_c, left_on='B2', right_on='C2A', how='inner')
    # Repliziere dataframe_a für die Anzahl der Zeilen in dataframe_b_c
    df_a_repeated_for_b_c = pandas.concat([dataframe_a] * dataframe_b_c.shape[0], ignore_index=True)
    dataframe_b_c["B14"] = "YN" * 50
    dataframe_b_c["C20"] = "YN" * 50
    dataframe_b_c["C21"] = "YN" * 50

    # Verbinde df_a_repeated_for_b_c horizontal mit dataframe_b_c
    dataframe_a_b_c = pandas.concat([df_a_repeated_for_b_c, dataframe_b_c], axis=1)
    dataframe_a_b_c["A1"] = "A"

    # save dataframe b to csv


def save_new_dataframes():
    dataframe_b.to_csv('B.csv', index=False)
    dataframe_c.to_csv('C.csv', index=False)
    #dataframe_b_c.to_csv('B_C.csv', index=False)
    dataframe_a_b_c.to_csv('A_B_C.csv', index=False)


#################################################################################################
# in spalte D1 in D muss immer die Konstante "D" stehen


#######D2########
# trage in D2 die einzigartigen werte aus B2 ein
dataframe_d['D2'] = dataframe_a_b_c['B2'].unique()

#######D3#######
# D3 hat die summe aller werte aus C19 abhängig von der kundennummer
dataframe_d['D3'] = dataframe_a_b_c.groupby('B2')['C19'].transform('sum')


#######D4#######
def compute_D4_grouped(group, df_d):
    # Initialize D4 value
    D4_value = 0.00

    # Check for "01" or "10" in A3
    if str(group['A3'].iloc[0]) in ['01', '10']:

        # Check if any value in B14 (range "01" to "30") is "Y"
        if any("Y" in s for s in group['B14'].str[0:30]):
            D4_value = group['C19'].sum()
        elif int(df_d[df_d['D2'] == group['B2'].iloc[0]]['D3'].iloc[0]) < 20 and all(group['C20'].str[0] == 'Y'):
            D4_value = df_d[df_d['D2'] == group['B2'].iloc[0]]['D3'].iloc[0]
        elif any("Y" in s for s in group['C20'].str[1:30]):
            D4_value = group['C19'].sum()
    else:
        D4_value = 0.00

    # Set D4 value in dataframe_d
    df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D4'] = D4_value


# group by B2 and apply the function compute_D4_grouped
dataframe_a_b_c.groupby('B2').apply(compute_D4_grouped, dataframe_d)


#######D5#############
def compute_D5_grouped(group, df_d):
    # Initialize D5 value
    D5_value = 0.00

    # Check for "01" or "10" in A3
    if str(group['A3'].iloc[0]) in ['01', '10']:
        # Calculate D3 divided by D4
        D3_value = df_d[df_d['D2'] == group['B2'].iloc[0]]['D3'].iloc[0]
        D4_value = df_d[df_d['D2'] == group['B2'].iloc[0]]['D4'].iloc[0]

        # Avoid division by zero
        if D4_value != 0:
            D5_value = D3_value / D4_value
    else:
        D5_value = 0.00

    # Set D5 value in dataframe_d
    df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D5'] = D5_value


dataframe_a_b_c.groupby('B2').apply(compute_D5_grouped, dataframe_d)


########################## D6 #############################
def compute_D6_grouped(group, df_d):
    # Initialize D6 value
    D6_value = 0.00

    # Check for "01" or "10" in A3
    if str(group['A3'].iloc[0]) in ['01', '10']:
        # Get the D5 value
        D5_value = df_d[df_d['D2'] == group['B2'].iloc[0]]['D5'].iloc[0]

        # Calculate the limit which is A4 * C5
        limit_value = group['A4'].iloc[0] * group['C5'].iloc[0]

        # Set D6 to be the minimum of D5 and the limit value
        D6_value = min(D5_value, limit_value)
    else:
        D6_value = 0.00

    # Set D6 value in dataframe_d
    df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D6'] = D6_value


dataframe_a_b_c.groupby('B2').apply(compute_D6_grouped, dataframe_d)


########################## D7 #############################


def compute_D7_grouped(group, df_d):
    # Initialize D7 value
    D7_value = 0.00

    # Check for "01" or "10" in A3
    if str(group['A3'].iloc[0]) in ['01', '10']:
        # Get the D5 and D6 values
        D5_value = df_d[df_d['D2'] == group['B2'].iloc[0]]['D5'].iloc[0]
        D6_value = df_d[df_d['D2'] == group['B2'].iloc[0]]['D6'].iloc[0]

        # Avoid division by zero
        if D6_value != 0:
            D7_value = D5_value / D6_value
    else:
        D7_value = 0.00

    # Set D7 value in dataframe_d
    df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D7'] = D7_value


dataframe_a_b_c.groupby('B2').apply(compute_D7_grouped, dataframe_d)


########################## D8 #############################
def compute_D8_grouped(group, df_d):
    # Check if C22 has a value and it's not "DE"
    D8_value = 0.00
    if pandas.notnull(group['C22'].iloc[0]) and group['C22'].iloc[0] != "DE":
        D8_value = group['C19'].sum()

    df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D8'] = D8_value


dataframe_a_b_c.groupby('B2').apply(compute_D8_grouped, dataframe_d)


########################## D9 #############################
def compute_D9_grouped(group, df_d):
    D9_value = 0.00
    if str(group['A3'].iloc[0]) == '20':
        limit_value = group['A5'].iloc[0] * group['C5'].iloc[0]
        D9_value = min(df_d[df_d['D2'] == group['B2'].iloc[0]]['D3'].iloc[0], limit_value)
    df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D9'] = D9_value


dataframe_a_b_c.groupby('B2').apply(compute_D9_grouped, dataframe_d)


########################## D10 #############################

def compute_D10_grouped(group, df_d):
    D10_value = 0.00
    if str(group['A3'].iloc[0]) in ["10", "20"]:
        D10_value = group[group['C27'] == 10]['C19'].sum()
    df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D10'] = D10_value


dataframe_a_b_c.groupby('B2').apply(compute_D10_grouped, dataframe_d)


########################## D11 #############################

def compute_D11_grouped(group, df_d):
    D11_value = 0.00
    if str(group['A3'].iloc[0]) in ['10', '20']:
        D11_value = group[group['C27'] == 20]['C19'].sum() - group['C26'].sum()
    df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D11'] = D11_value


dataframe_a_b_c.groupby('B2').apply(compute_D11_grouped, dataframe_d)


########################## D14A #############################

def compute_D14A_grouped(group, df_d):
    D14A_value = 0.00
    if str(group['A3'].iloc[0]) in ["10", "20"]:
        # Sum of debitorische Kontosalden from C19
        D14A_value = -group['C19'].sum()
    else:
        D14A_value = 0.00

    df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D14A'] = D14A_value


dataframe_a_b_c.groupby('B2').apply(compute_D14A_grouped, dataframe_d)


########################## D12A #############################
def compute_D12A_grouped(group, df_d):
    D12A_value = 0.00
    if str(group['A3'].iloc[0]) in ["10", "20"]:

        wert1 = df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D3'].iloc[0]
        wert2 = df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D10'].iloc[0]
        wert3 = df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D14A'].iloc[0]
        wert4 = max(df_d.loc[df_d['D2'] == group['B2'].iloc[0], ['D6', 'D9', 'D11']].iloc[0])
        HW1 = wert1 - wert2 + wert3 - wert4

        wert5 = df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D6'].iloc[0] + df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D9'].iloc[0];
        if wert5 != 0:
            limit_value = (group['A6C'].iloc[0] * group['C5'].iloc[0]) / wert5
            D12A_value = min(HW1, limit_value)
        else:
            D12A_value = HW1
        if D12A_value < 0:
            D12A_value = 0.00

    df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D12A'] = D12A_value


dataframe_a_b_c.groupby('B2').apply(compute_D12A_grouped, dataframe_d)


########################## D12B #############################
def compute_D12B_grouped(group, df_d):
    D12B_value = 0.00

    if str(group['A3'].iloc[0]) in [10, 20] and pandas.notnull(group['A8'].iloc[0]):
        # Berechne HW2
        HW2 = group[(group['C27'].isin(['01', '90'])) & (group['C21'].str[18] == 'Y')]['C19'].sum()
        wert1 = df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D3'].iloc[0]
        wert2 = df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D10'].iloc[0]
        wert3 = df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D14A'].iloc[0]
        wert4 = max(df_d.loc[df_d['D2'] == group['B2'].iloc[0], ['D6', 'D9', 'D11']].iloc[0])
        HW1 = wert1 - wert2 + wert3 - wert4
        # Berechne HW3
        HW3_1 = group[(group['C27'] == '90') & (group['C21'].str[10] == 'N') & (group['C21'].str[18] == 'N')]['C19'].sum()
        HW3_2 = group[group['C27'] == '20']['C19'].sum()
        HW3 = HW3_1 + HW3_2

        # Werte für die Berechnung
        D12A_value = df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D12A'].iloc[0]
        D6_value = df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D6'].iloc[0]
        D9_value = df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D9'].iloc[0]
        A9_value = group['A9'].iloc[0]
        C5_value = group['C5'].iloc[0]

        # Berechne die drei möglichen Werte für D12B
        value1 = HW1 / D12A_value
        value2 = HW2 / (D6_value + D9_value / HW3) if HW3 != 0 and (D6_value + D9_value / HW3) > 0 else HW2
        value3 = A9_value * C5_value / (D6_value + D9_value + D12A_value)

        # Setze D12B auf den kleinsten Wert
        D12B_value = min(value1, value2, value3)

    df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D12B'] = D12B_value


dataframe_a_b_c.groupby('B2').apply(compute_D12B_grouped, dataframe_d)

########################## D12C #############################
def compute_D12C_grouped(group, df_d):
    D12C_value = 0.00

    # Berechne HW4
    HW4 = group[(group['C27'].isin(['01', '90'])) & (group['C21'].str[10] == 'Y')]['C19'].sum()

    # Berechne HW5
    HW5_1 = group[(group['C27'] == '90') & (group['C21'].str[10] == 'N')]['C19'].sum()
    HW5_2 = group[group['C27'] == '20']['C19'].sum()
    HW5 = HW5_1 + HW5_2

    # Berechne HW1
    wert1 = df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D3'].iloc[0]
    wert2 = df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D10'].iloc[0]
    wert3 = df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D14A'].iloc[0]
    wert4 = max(df_d.loc[df_d['D2'] == group['B2'].iloc[0], ['D6', 'D9', 'D11']].iloc[0])
    HW1 = wert1 - wert2 + wert3 - wert4

    if str(group['A3'].iloc[0]) in ["10", "20"] and any(group['C21'].str[10] == 'Y') and HW1 < int(group['A6C'].iloc[0]) * group['C5'].sum(): #welcher c5 wert soll genommen werden
        # Werte für die Berechnung
        D12A_value = df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D12A'].iloc[0]
        D12B_value = df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D12B'].iloc[0]
        D6_value = df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D6'].iloc[0]
        D9_value = df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D9'].iloc[0]
        A6_value = group['A6C'].iloc[0]
        C5_value = group['C5'].iloc[0]
        A7_value = group['A7'].iloc[0]
        
        wert2 = HW4 / ((D6_value + D9_value) / HW5) if (D6_value + D9_value) / HW5 > 0 else HW4
        wert3 = A7_value * C5_value / (D6_value + D9_value + D12A_value + D12B_value) 

        # Setze D12C auf den kleinsten Wert
        D12C_value = min(wert1, wert2, wert3)
        if D12C_value < 0:
            D12C_value = 0.00
        

    
    df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D12C'] = D12C_value



dataframe_a_b_c.groupby('B2').apply(compute_D12C_grouped, dataframe_d)


########################## D13 #############################


def compute_D13_grouped(group, df_d):
    D13_value = 0.00
    if str(group['A3'].iloc[0]) in ["10", "20"]:
        D12A_value = df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D12A'].iloc[0]
        D12B_value = df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D12B'].iloc[0]
        D12C_value = df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D12C'].iloc[0]
        D13_value = D12A_value + D12B_value + D12C_value
    df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D13'] = D13_value

dataframe_a_b_c.groupby('B2').apply(compute_D13_grouped, dataframe_d)

########################## D15 #############################

def compute_D15_grouped(group, df_d):
    D15_value = 0.00
    valid_entries = group[pandas.notnull(group['C23'])]
    D15_value = valid_entries['C19'].sum()
    df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D15'] = D15_value

dataframe_a_b_c.groupby('B2').apply(compute_D15_grouped, dataframe_d)




###############################################################
dataframe_d.to_csv('D.csv', index=False)


###################### Dataframe E ############################
# Erstelle ein leeres DataFrame für E
dataframe_e = pandas.DataFrame(index=[0])

# Setze die Werte für die Spalten in E
dataframe_e.at[0, 'E1'] = 'E'
# E2 wird freigelassen, wie du erwähnt hast
dataframe_e.at[0, 'E3'] = dataframe_d['D3'].sum()
dataframe_e.at[0, 'E4'] = dataframe_d['D4'].sum()
dataframe_e.at[0, 'E5'] = dataframe_d['D5'].sum()
dataframe_e.at[0, 'E6'] = dataframe_d['D6'].sum()
dataframe_e.at[0, 'E7'] = dataframe_d['D7'].sum()
dataframe_e.at[0, 'E8'] = dataframe_d['D8'].sum()
dataframe_e.at[0, 'E9'] = dataframe_d['D9'].sum()
dataframe_e.at[0, 'E10'] = dataframe_d['D10'].sum()
dataframe_e.at[0, 'E11'] = dataframe_d['D11'].sum()
dataframe_e.at[0, 'E12A'] = dataframe_d['D12A'].sum()
dataframe_e.at[0, 'E12B'] = dataframe_d['D12B'].sum()
dataframe_e.at[0, 'E12C'] = dataframe_d['D12C'].sum()
dataframe_e.at[0, 'E13'] = dataframe_d['D13'].sum()
dataframe_e.at[0, 'E14'] = dataframe_d['D14A'].sum()
dataframe_e.at[0, 'E15'] = dataframe_d['D15'].sum()


dataframe_e.to_csv('E.csv', index=False)


#datei schreiben:
with open("output.txt", "w") as file:
    file.write("\t".join(dataframe_a.iloc[0].astype(str)) + "\n")
    # Gruppieren nach allen B-Spalten
    grouped = dataframe_a_b_c.groupby(list(dataframe_a_b_c.columns[dataframe_a_b_c.columns.str.startswith('B')]))
    for _, group in grouped:
        # Schreibe die B-Werte in die Datei
        b_values = group.iloc[0][dataframe_a_b_c.columns.str.startswith('B')].astype(str)
        file.write(','.join(b_values) + '\n')

             # Schreibe die C-Werte in die Datei
        for _, row in group.iterrows():
            c_values = row[dataframe_a_b_c.columns.str.startswith('C')].astype(str)
            file.write(','.join(c_values) + '\n')

        b2_value = group['B2'].iloc[0]
        d_row = dataframe_d[dataframe_d['D2'] == b2_value]
        d_values = d_row.iloc[0].astype(str)
        file.write(','.join(d_values) + '\n')
        
        
    for _, row in dataframe_e.iterrows():
        e_values = row.astype(str)
        file.write(','.join(e_values) + '\n')
