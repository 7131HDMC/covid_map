import pandas as pd

"""## Importing the dataset and break export Brazil and States"""
df = pd.read_csv("data/HIST_PAINEL_COVIDBR_2022_Parte1_09abr2022.csv", sep=";")

states_df = df[( (~df["estado"].isna()) & (df["codmun"].isna()) )]
brazil_df = df[df["regiao"] == "Brasil"]

states_df.to_csv("data/states_df.csv")
brazil_df.to_csv("data/brazil_df.csv")
