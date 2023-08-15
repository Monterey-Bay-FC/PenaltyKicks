import pandas as pd
penalties = pd.read_csv('PenaltyData.csv')
#print(penalties.head())

print(penalties["Player"].value_counts())
