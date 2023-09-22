import pandas 
import numpy as np


dataframe_a = pandas.read_csv('A.csv', sep=',', header=0)
dataframe_b = pandas.read_csv('B.csv', sep=',', header=0)
dataframe_c = pandas.read_csv('C.csv', sep=',', header=0)
dataframe_d = pandas.read_csv('D.csv', sep=',', header=0)
dataframe_e = pandas.read_csv('E.csv', sep=',', header=0)

#kundennummer bei B2 und C2A verbinde dort nicht alle C2A sind in B2 enthalten
dataframe_b['B2'] = dataframe_b['B2'].astype(str)
dataframe_c['C2A'] = dataframe_c['C2A'].astype(str)


dataframe_b = pandas.DataFrame(np.random.randint(0, 75, size=(100, 16)), columns=dataframe_b.columns)

# Setting the first 20 values in column B2 to range from 0 to 19
dataframe_b.loc[:19, "B2"] = np.arange(20)
dataframe_c = pandas.DataFrame(np.random.randint(0, 200, size=(150, 28)), columns=dataframe_c.columns)

dataframe_b["B1"] = "B"
dataframe_c["C1"] = "C"

#verbinde die den dataframe B und C anhand der werte aus B2 und C2A
dataframe_b_c = pandas.merge(dataframe_b, dataframe_c, left_on='B2', right_on='C2A', how='inner')
# Repliziere dataframe_a für die Anzahl der Zeilen in dataframe_b_c
df_a_repeated_for_b_c = pandas.concat([dataframe_a]*dataframe_b_c.shape[0], ignore_index=True)
dataframe_b_c["B14"] = "N"*50
dataframe_b_c["C20"] = "N"*50
dataframe_b_c["C21"] = "N"*50

# Verbinde df_a_repeated_for_b_c horizontal mit dataframe_b_c
dataframe_a_b_c = pandas.concat([df_a_repeated_for_b_c, dataframe_b_c], axis=1)

dataframe_a_b_c["A1"] = "A"
#save dataframe b to csv
dataframe_b.to_csv('B.csv', index=False)
dataframe_c.to_csv('C.csv', index=False)
dataframe_b_c.to_csv('B_C.csv', index=False)
dataframe_a_b_c.to_csv('A_B_C.csv', index=False)


#################################################################################################
#in spalte D1 in D muss immer die Konstante "D" stehen

#trage in D2 die einzigartigen werte aus B2 ein
dataframe_d['D2'] = dataframe_a_b_c['B2'].unique()

#######D3#######
#D3 hat die summe aller werte aus C19 abhängig von der kundennummer
dataframe_d['D3'] = dataframe_a_b_c.groupby('B2')['C19'].transform('sum')

def compute_D4_grouped(group):
    # Set initial value of D4 for the group
    D4_value = 0.00

    # For institutes with value "01" or "10" in field A3
    if group['A3'].iloc[0] in ['01', '10']:
        # Check if any value in B14 (range "01" to "30") is "Y"
        if "Y" in group['B14'][0:30]:
            D4_value = group['C19'].sum()
            
    
        # Check if D3 is less than 20 and all values in C20 at position "01" are "Y"
        elif dataframe_d[dataframe_d['D2'] == group['B2'].iloc[0]]['D3'].iloc[0] < 20 and all(group['C20'].str.split("").apply(lambda x: x[0] == 'Y')):
            D4_value = dataframe_d[dataframe_d['D2'] == group['B2'].iloc[0]]['D3'].iloc[0]
        # Check if any value in C20 (range "02" to "30") is "Y"
        elif any(group['C20'].str.split('').apply(lambda x: 'Y' in x[1:30])):
            D4_value = group['C19'].sum()
        else:
            D4_value = 0.00
    else:
        D4_value = 0.00
    # Set D4 value for the entire group
    dataframe_d[dataframe_d['D2'] == group['B2'].iloc[0]]["D4"].iloc[0] = D4_value
    return group
 




dataframe_d['D1'] = 'D'
dataframe_d.to_csv('D.csv', index=False)
print(dataframe_b_c.head())
