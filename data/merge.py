import pandas as pd

df_eth = pd.read_csv("./ethiopian-tbills.csv")
df_ksh = pd.read_csv("./kenya-pdfs/kenyan-tbills.csv")

combined_df = pd.concat([df_ksh, df_eth], ignore_index=True)
combined_df.to_csv("master.csv", index=False)
