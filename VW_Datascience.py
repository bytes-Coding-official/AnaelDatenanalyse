import pandas
import numpy as np

dataframe_a = pandas.read_csv('A.csv', sep=',', header=0)
dataframe_b = pandas.read_csv('B.csv', sep=',', header=0)
dataframe_c = pandas.read_csv('C.csv', sep=',', header=0)
dataframe_d = pandas.read_csv('D.csv', sep=',', header=0)
dataframe_e = pandas.read_csv('E.csv', sep=',', header=0)
dataframe_a_b_c = pandas.read_csv('A_B_C.csv', sep=',', header=0)
dataframe_d['D1'] = 'D'
dataframe_b["B1"] = "B"
dataframe_c["C1"] = "C"
# drop all values from dataframe_d
dataframe_d = dataframe_d.iloc[0:0]
# kundennummer bei B2 und C2A verbinde dort nicht alle C2A sind in B2 enthalten
dataframe_b['B2'] = dataframe_b['B2'].astype(str)
dataframe_c['C2A'] = dataframe_c['C2A'].astype(str)


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
    dataframe_b_c.to_csv('B_C.csv', index=False)
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
        value1 = HW1/D12A_value
        value2 = HW2 / (D6_value + D9_value / HW3) if HW3 != 0 and (D6_value + D9_value / HW3) > 0 else HW2
        value3 = A9_value * C5_value / (D6_value + D9_value + D12A_value)

        # Setze D12B auf den kleinsten Wert
        D12B_value = min(value1, value2, value3)

    df_d.loc[df_d['D2'] == group['B2'].iloc[0], 'D12B'] = D12B_value

dataframe_a_b_c.groupby('B2').apply(compute_D12B_grouped, dataframe_d)


###############################################################
dataframe_d.to_csv('D.csv', index=False)
