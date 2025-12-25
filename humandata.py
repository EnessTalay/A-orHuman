import feedparser
import pandas as pd

BASE_URL = "http://export.arxiv.org/api/query?"

search_query = "cat:cs.CL"
start = 1000
max_results = 1000

query = (
    f"search_query={search_query}"
    f"&start={start}"
    f"&max_results={max_results}"
)

feed = feedparser.parse(BASE_URL + query)

data = []
id_counter = 1

for entry in feed.entries:
    abstract = entry.summary.replace("\n", " ").strip()
    word_count = len(abstract.split())

    if 100 <= word_count <= 350:
        data.append({
            "id": id_counter,
            "text": abstract,
            "label": "human",
            "source": "arxiv"
        })
        id_counter += 1

df = pd.DataFrame(data)
df.to_csv("human_part4.csv", index=False, encoding="utf-8")


print(f"{len(df)} adet abstract kaydedildi.")
