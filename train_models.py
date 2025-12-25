import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
import joblib
import os

# 1. Verileri yükle
df_human = pd.read_excel("data/humanclean.xlsx")
df_ai = pd.read_excel("data/aiclean.xlsx")

# 2. Birleştir ve etiketle
df = pd.concat([df_human, df_ai], ignore_index=True)
df['label'] = df['label'].map({'human': 0, 'ai': 1})
df = df.dropna()

X = df['abstract']
y = df['label']

# 3. Vectorizer (8000 özellik)
vectorizer = TfidfVectorizer(max_features=8000, stop_words='english', ngram_range=(1, 2))
X_tfidf = vectorizer.fit_transform(X)

# 4. VERİYİ BÖL (DİKKAT: Burada X_tfidf kullanıyoruz, X_final DEĞİL!)
X_train, X_test, y_train, y_test = train_test_split(
    X_tfidf, y, test_size=0.2, stratify=y, random_state=42
)

# 5. Modelleri eğit
print("SİSTEM: Modeller eğitiliyor...")
lr_model = LogisticRegression(max_iter=1000).fit(X_train, y_train)
svm_model = LinearSVC(max_iter=5000).fit(X_train, y_train)
nb_model = MultinomialNB().fit(X_train, y_train)

# 6. Kaydet
os.makedirs("models", exist_ok=True)
joblib.dump(vectorizer, "models/vectorizer.joblib")
joblib.dump(lr_model, "models/lr_model.joblib")
joblib.dump(svm_model, "models/svm_model.joblib")
joblib.dump(nb_model, "models/nb_model.joblib")

print("✅ YENİ MODELLER BAŞARIYLA KAYDEDİLDİ!")