from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import os
import warnings

app = Flask(__name__)
CORS(app)   # 🔥 THIS FIXES CORS

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
model = joblib.load(MODEL_PATH)

# Silence sklearn's feature-name warning when predicting with raw numpy arrays.
warnings.filterwarnings("ignore", message="X does not have valid feature names*")

@app.route("/")
def home():
    return jsonify({"status": "Backend running"})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400

    try:
        # Build the feature vector in the exact order the model was trained on (if available).
        # Use a DataFrame so sklearn Pipelines keep feature names (and any preprocessors work reliably).
        expected_attr = getattr(model, "feature_names_in_", None)
        expected = list(expected_attr) if expected_attr is not None else ["Age", "Number of sexual partners", "Smokes", "STDs", "Dx"]
        row = {name: float(data[name]) for name in expected}
        X = pd.DataFrame([row], columns=expected)

        # If the model supports probabilities, allow an explicit threshold override.
        # Default is 0.5 (same as sklearn's default decision rule for logistic regression).
        threshold = float(data.get("_threshold", os.getenv("PREDICT_THRESHOLD", "0.5")))

        response = {"threshold": threshold}
        if hasattr(model, "predict_proba"):
            # sklearn's predict_proba columns align with model.classes_, so map explicitly to class=1
            classes = list(getattr(model, "classes_", []))
            idx_1 = classes.index(1) if 1 in classes else 1
            proba = float(model.predict_proba(X)[0][idx_1])
            response["probability"] = proba
            response["prediction"] = int(proba >= threshold)
        else:
            prediction = model.predict(X)
            response["prediction"] = int(prediction[0])
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
