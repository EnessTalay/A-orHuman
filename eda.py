import pandas as pd
import matplotlib.pyplot as plt

df_human = pd.read_excel("data/humanclean.xlsx")
df_ai = pd.read_excel("data/aiclean.xlsx")

df = pd.concat([df_human, df_ai], ignore_index=True)
df['label'] = df['label'].map({'human': 0, 'ai': 1})
df = df.dropna()

# Text length
df['text_length'] = df['abstract'].apply(len)

human_lengths = df[df['label'] == 0]['text_length']
ai_lengths = df[df['label'] == 1]['text_length']

print("Human text length stats:")
print(human_lengths.describe())

print("\nAI text length stats:")
print(ai_lengths.describe())


plt.hist(human_lengths, bins=50, alpha=0.6, label='Human')
plt.hist(ai_lengths, bins=50, alpha=0.6, label='AI')
plt.legend()
plt.title("Text Length Distribution (EDA)")
plt.xlabel("Length")
plt.ylabel("Count")
plt.show()
