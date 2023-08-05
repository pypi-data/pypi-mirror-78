import pandas as pd

df = pd.read_csv(f"https://raw.githubusercontent.com/adamerose/datasets/master/mi_manufacturing.csv")
df.sort_index(level=0, kind='mergesort')
