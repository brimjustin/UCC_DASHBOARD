import pandas as pd
from pathlib import Path


# TDF CSV to DF
tdf_csv = Path(__file__).parents[1] / 'UCC_DASHBOARD/data/Transformed_DF.csv'
tdf = pd.read_csv(tdf_csv)

# KDF CSV to DF
kdf_csv = Path(__file__).parents[1] / 'UCC_DASHBOARD/data/kubota_hp.csv'
kdf = pd.read_csv(kdf_csv)

# DDF CSV to DF
ddf_csv = Path(__file__).parents[1] / 'UCC_DASHBOARD/data/deere_hp.csv'
ddf = pd.read_csv(ddf_csv)

# KBE CSV to DF
kbe_csv = Path(__file__).parents[1] / 'UCC_DASHBOARD/data/KBE_Transformed_DF.csv'
kbe = pd.read_csv(kbe_csv)


kdf.reset_index(inplace=True)
ddf.reset_index(inplace=True)
kdf.drop(kdf.columns[0], axis=1, inplace=True)
ddf.drop(ddf.columns[0], axis=1, inplace=True)
kdf['hp'] = kdf['hp'].str.replace(r"\s*hp.*$", "")
ddf['hp'] = ddf['hp'].str.replace(r"\s*hp.*$", "")

kdf['hp'].fillna(0, inplace=True)
ddf['hp'].fillna(0, inplace=True)
kdf['hp'] = kdf['hp'].astype(tdf['hp'].dtype)
ddf['hp'] = ddf['hp'].astype(tdf['hp'].dtype)
kbe['hp'] = kbe['hp'].astype(tdf['hp'].dtype)

for i, row in tdf.iterrows():
    kdf_hp = kdf.loc[kdf['model'] == row['model'], 'hp'].values
    if kdf_hp.size != 0 and pd.notna(kdf_hp[0]) and kdf_hp[0] != 0:
        tdf.at[i, 'hp'] = kdf_hp[0]

for i, row in tdf.iterrows():
    ddf_hp = ddf.loc[ddf['model'] == row['model'], 'hp'].values
    if ddf_hp.size != 0 and pd.notna(ddf_hp[0]) and ddf_hp[0] != 0:
        tdf.at[i, 'hp'] = ddf_hp[0]

merged_df = pd.concat([tdf, kbe], ignore_index=True)


merged_df.to_csv(path_or_buf=f"/Users/mac/Desktop/BRIM-DATA/UCC_DASHBOARD/data/merged_tdf.csv",
                 index=False)
