import pandas as pd

df = pd.read_csv("human_part4.csv")

bad_rows = []

for i, text in enumerate(df["text"].astype(str)):
    if sum(text.count(s) for s in ["$", "\\", "{", "}", "^", "_"]) >= 10:
        bad_rows.append(i + 2)  # Excel row number

print(bad_rows)
print("Toplam:", len(bad_rows))