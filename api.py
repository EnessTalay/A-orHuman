from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(title="Human vs AI Text Detection API")

# ---- MODELLERİ YÜKLE ----
try:
    # Yeni eğittiğin 8000 özellikli modelleri yüklüyoruz
    vectorizer = joblib.load("models/vectorizer.joblib")
    models = {
        "lr": joblib.load("models/lr_model.joblib"),
        "nb": joblib.load("models/nb_model.joblib"),
        "svm": joblib.load("models/svm_model.joblib")
    }
    print("SİSTEM: 8000 özellikli yeni modeller başarıyla yüklendi.")
except Exception as e:
    print(f"HATA: Modeller yüklenemedi: {e}")

class TextRequest(BaseModel):
    text: str

@app.post("/predict")
def predict(request: TextRequest):
    # 1. Metni vektöre çevir (Artık hstack veya text_length YOK!)
    # Bu satır tam olarak 8000 özellik üretir.
    text_vec = vectorizer.transform([request.text])
    
    results = {}
    all_ai_percents = []

    # 2. Modellerle Tahmin Yap
    for name, model in models.items():
        # Tahmin (0 veya 1)
        raw_pred = int(model.predict(text_vec)[0])
        
        # Olasılık/Yüzde hesaplama (Barların hareket etmesi için)
        try:
            if hasattr(model, "predict_proba"):
                # LR ve NB için
                proba = model.predict_proba(text_vec)[0][1]
                ai_percent = int(proba * 100)
            else:
                # SVM için barların tahmine göre oynamasını sağlar
                df_val = model.decision_function(text_vec)[0]
                ai_percent = int(100 / (1 + np.exp(-df_val)))
        except:
            ai_percent = 95 if raw_pred == 1 else 5

        label = "AI" if raw_pred == 1 else "Human"
        results[name] = {"prediction": label, "ai_percent": ai_percent}
        all_ai_percents.append(ai_percent)

    # 3. Genel Sonuç (Modellerin Ortalaması)
    final_ai_percent = int(np.mean(all_ai_percents))
    final_label = "AI" if final_ai_percent > 50 else "Human"

    return {
        "final_prediction": final_label,
        "final_ai_percent": final_ai_percent,
        "models": results
    }

@app.get("/")
def root():
    return {"status": "API Hazır ve Yeni Modeller Aktif"}