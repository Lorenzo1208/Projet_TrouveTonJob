import pandas as pd


df = pd.read_json("data.json")

df['salaire'] = df['lieu'].apply(lambda x: x[1] if len(x) > 1 else '')
df['lieu'] = df['lieu'].apply(lambda x : x[0])

df = df.apply(lambda c : c.apply(lambda x : ','.join([s.strip("\n ").lower() for s in (x.split(',') if type(x) != list else x)])))

df.to_csv("data_test1.csv", index=False)
