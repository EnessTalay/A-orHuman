def choose_model(text):
    length = len(text)

    if length < 700:
        return "nb"
    elif length < 1000:
        return "lr"
    else:
        return "lr"

def predict_text(text, vectorizer, models):
    model_key = choose_model(text)

    text_vec = vectorizer.transform([text])
    text_len = [[len(text)]]

    from scipy.sparse import hstack
    final_vec = hstack([text_vec, text_len])

    if model_key == "nb":
        prediction = models["nb"].predict(text_vec)
    else:
        prediction = models[model_key].predict(final_vec)

    return prediction[0], model_key
