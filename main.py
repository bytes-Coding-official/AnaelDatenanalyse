import pandas

# lade nun die daten aus der datei in ein pandas dataframe
dfgut = pandas.read_csv('b2_contract.csv', sep=',', header=None, names=['B2-Number', 'Kunden_Nummer'])
print(dfgut)
# #gruppiere nach den B2-Nummern und zähle die Anzahl der Einträge
# #speichere das Ergebnis in einer neuen Variable
# df2 = dfgut.groupby('B2-Number')
# 
# #order by contract number add new column with the amount of contracts
# df3 = df2['Kunden_Nummer'].count().reset_index(name='Amount of Contracts').sort_values(['Amount of Contracts'], ascending=False)
# 
# #gib alle B2-Nummern aus, die 2 verträge haben
# df4 = df3.loc[df3['Amount of Contracts'] == 2]
# #print(df4)
# 
# #finde alle vertragsnummern die zu den B2-Nummern gehören, die 2 verträge haben
# df5 = dfgut.loc[dfgut['B2-Number'].isin(df4['B2-Number'])]
# #gruppiere nach den B2-Nummern und gib die vertragsnummern mit dazu
# df6 = df5.groupby('B2-Number')['Kunden_Nummer'].apply(list).reset_index(name='Kunden_Nummers')
# #print(df6)
# 
# #nimm alle vertragsnummern aus der liste und speichere sie in einer neuen liste
# df7 = df6['Kunden_Nummers'].tolist()
# #print(df7)
# 
# 
# #einzelne Vertragsnummer:
# nummer = df7[0][0]
# 
# #finde alle B2 Nummern, die zu der Vertragsnummer gehören
# df8 = dfgut.loc[dfgut['Kunden_Nummer'] == nummer]
# df9 = df8.groupby('B2-Number')['Kunden_Nummer'].apply(list).reset_index(name='Kunden_Nummers')
# #print(df9)
# 
# # 
# # Here's a brief explanation of the Python code you provided. The programming language used in the code is Python.
# # The code starts by importing the pandas library, which is often used for data manipulation and analysis.
# #     df = pandas.read_csv('b2_contract.csv', sep=',', names=['B2-Number', 'Kunden_Nummer']) The .csv file 'b2_contract.csv' is read here using the pandas 'read_csv' function and is assigned to the dataframe 'df'. It uses a comma separator and the columns are named 'B2-Number' and 'Kunden_Nummer'.
# # df2 = df.groupby('B2-Number') The dataframe is grouped by the 'B2-Number' and stored in a new dataframe 'df2'.
# # df3 = df2['Kunden_Nummer'].count().reset_index(name='Amount of Contracts').sort_values(['Amount of Contracts'], ascending=False) Here, for each 'B2-Number', the count of 'Kunden_Nummer' is taken and stored in a new column 'Amount of Contracts'. The dataframe is then sorted in descending order based on the 'Amount of Contracts'.
# # df4 = df3.loc[df3['Amount of Contracts'] == 2] This line filters out and returns the rows where 'Amount of Contracts' is equal to 2.
# # df5 = df.loc[df['B2-Number'].isin(df4['B2-Number'])] This line filters the original dataframe 'df' to include only the rows where 'B2-Number' exists in 'df4' dataframe.
# # df6 = df5.groupby('B2-Number')['Kunden_Nummer'].apply(list).reset_index(name='Kunden_Nummers') This groups 'df5' dataframe by 'B2-Number' and get the list of 'Kunden_Nummer' for each group. Output is stored in a new dataframe 'df6'.
# # df7 = df6['Kunden_Nummers'].tolist() Here, all 'Kunden_Nummers' are converted to a list and assigned to 'df7'.
# # nummer = df7[0][0] This gets the first element of the 0th list in df7 and assigns to 'nummer'.
# # df8 = df.loc[df['Kunden_Nummer'] == nummer] This gets all rows from 'df' dataframe where 'Kunden_Nummer' equals to 'nummer'.
# # df9 = df8.groupby('B2-Number')['Kunden_Nummer'].apply(list).reset_index(name='Kunden_Nummers') This groups 'df8' dataframe by 'B2-Number' and get the list of 'Kunden_Nummer' for each group. Output is stored in a new dataframe 'df9'.
# # Finally, the script prints out 'df9', showing the B2 numbers that match the individual contract number 'nummer'.
# # Thus, this script manipulates a dataframe containing contracts, grouping and sorting them according to the contract number, extracting specific data and contract numbers from it.
# 
# 
# #importiere die tabelle tabelle_a in ein pandas dataframe
# #print(df)
# 
# #kombiniere nun die erste zeile aus dfgut mit der ersten zeile aus df heißt erst kommen alle werte aus df und darunter die werte aus dfgut falls werte fehlen fülle diese mit null die werte auf dfgut sollen unter den werten von df stehen nicht daneben
# #df1, df2, df3, df4
# #dfgut1, dfgut2, null, null
# #so in der art
df = pandas.read_csv('tabelle_a.csv', sep=',', header=None)
dfB = pandas.read_csv('b2_contract.csv', sep=',', header=None)

# Füge fehlende Spalten mit NaN zu dfB hinzu
for col in df.columns:
    if col not in dfB.columns:
        dfB[col] = None
# Sortiere die Spalten von dfB entsprechend der Reihenfolge von df
dfB = dfB[df.columns]
# Staple die DataFrames zeilenweise
result = pandas.concat([df, dfB]).sort_index(kind="merge").reset_index(drop=True)
print(result)

# It imports the pandas library, a widely used data manipulation and analysis tool in Python.
# It reads two CSV files ('tabelle_a.csv' and 'b2_contract.csv') into pandas DataFrames df and dfB respectively, with no header (i.e., column names are not provided in the CSV file).
# Then, the code iterates over each column of the df DataFrame. If the column does not exist in the dfB DataFrame, it adds that column to dfB with a value of None for every row. Essentially, this looks to harmonize the DataFrames so they have identical column structure.
# It rearranges the columns in dfB to match the column order of the original df DataFrame.
# Then it concatenates df and dfB row-wise; this means it combines these two DataFrames, appending the rows of dfB to the rows of df, resulting in a larger DataFrame.
# After that, the combined DataFrame is sorted by index. The kind="merge" argument tells pandas to use merge sort for sorting.
#     The reset_index(drop=True) operation is then used to reset the index of the DataFrame to default integer values and drop=True drops the current index of the DataFrame and replaces it with an index of increasing integers.
# Finally, this resulting combined and sorted DataFrame is printed to the console.
