import pandas


#lade nun die daten aus der datei in ein pandas dataframe
df = pandas.read_csv('b2_contract.csv', sep=',', names=['B2-Number', 'Kunden_Nummer'])
#gruppiere nach den B2-Nummern und zähle die Anzahl der Einträge
#speichere das Ergebnis in einer neuen Variable
df2 = df.groupby('B2-Number')

#order by contract number add new column with the amount of contracts
df3 = df2['Kunden_Nummer'].count().reset_index(name='Amount of Contracts').sort_values(['Amount of Contracts'], ascending=False)

#gib alle B2-Nummern aus, die 2 verträge haben
df4 = df3.loc[df3['Amount of Contracts'] == 2]
print(df4)

#finde alle vertragsnummern die zu den B2-Nummern gehören, die 2 verträge haben
df5 = df.loc[df['B2-Number'].isin(df4['B2-Number'])]
#gruppiere nach den B2-Nummern und gib die vertragsnummern mit dazu
df6 = df5.groupby('B2-Number')['Kunden_Nummer'].apply(list).reset_index(name='Kunden_Nummers')
print(df6)

#nimm alle vertragsnummern aus der liste und speichere sie in einer neuen liste
df7 = df6['Kunden_Nummers'].tolist()
print(df7)


#einzelne Vertragsnummer:
nummer = df7[0][0]

#finde alle B2 Nummern, die zu der Vertragsnummer gehören
df8 = df.loc[df['Kunden_Nummer'] == nummer]
df9 = df8.groupby('B2-Number')['Kunden_Nummer'].apply(list).reset_index(name='Kunden_Nummers')
print(df9)
