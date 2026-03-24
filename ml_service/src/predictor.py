import os
import joblib
import pandas as pd
from src.feature_pipeline import build_feature_dict, FINAL_FEATURE_ORDER

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")

MODEL_PATH = os.path.join(ARTIFACTS_DIR, "model.pkl")
FEATURE_NAMES_PATH = os.path.join(ARTIFACTS_DIR, "feature_names.pkl")


def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")
    return joblib.load(MODEL_PATH)


def load_feature_names():
    if not os.path.exists(FEATURE_NAMES_PATH):
        raise FileNotFoundError(f"Feature names file not found at: {FEATURE_NAMES_PATH}")
    return joblib.load(FEATURE_NAMES_PATH)


def prepare_input_dataframe(url: str) -> pd.DataFrame:
    feature_dict = build_feature_dict(url)

    feature_names = load_feature_names()

    input_data = {feature: feature_dict[feature] for feature in feature_names}
    input_df = pd.DataFrame([input_data])

    return input_df


def predict_url(url: str) -> dict:
    model = load_model()
    input_df = prepare_input_dataframe(url)

    prediction = model.predict(input_df)[0]

    probability = None
    if hasattr(model, "predict_proba"):
        probas = model.predict_proba(input_df)[0]
        probability = float(max(probas))

    label = "Legitimate" if prediction == 1 else "Phishing"
    risk_level = "Low" if prediction == 1 else "High"

    return {
        "url": url,
        "prediction": int(prediction),
        "label": label,
        "risk_level": risk_level,
        "probability": probability,
        "features": input_df.to_dict(orient="records")[0]
    }


if __name__ == "__main__":
    user_url = input("Enter URL: ").strip()
    result = predict_url(user_url)

    print("\nPrediction Result:")
    print(f"URL: {result['url']}")
    print(f"Prediction: {result['label']}")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Probability: {result['probability']}")

    print("\nExtracted Features:")
    for key, value in result["features"].items():
        print(f"{key}: {value}")