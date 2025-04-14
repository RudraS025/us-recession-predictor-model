import joblib
from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

logger.info("Attempting to load the model...")
try:
    model = joblib.load('vertex_model.joblib')
    logger.info(f"✅ Model loaded successfully. Type: {type(model)}")
except Exception as e:
    logger.error(f"❌ Error loading model: {e}")
    model = None
    # Optionally, re-raise the exception to see it in the server logs (if enabled)
    # raise e

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded.'}), 500
    try:
        data = request.get_json()
        # ... (rest of your prediction logic) ...
        prediction = model.predict(input_data).tolist()
        return jsonify({'prediction': prediction})
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        return jsonify({'error': f'Error during prediction: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)