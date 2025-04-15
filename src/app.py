import os
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Update the model path to point to the notebooks sub-folder
logger.info("Attempting to load the model...")
try:
    MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../notebooks/vertex_model.joblib')
    model = joblib.load(MODEL_PATH)
    logger.info(f"✅ Model loaded successfully. Type: {type(model)}")
except FileNotFoundError:
    logger.error(f"❌ Model file not found at {MODEL_PATH}")
    model = None
except Exception as e:
    logger.error(f"❌ Error loading model: {e}")
    model = None

@app.route('/', methods=['GET'])
def index():
    return "US Recession Prediction API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded.'}), 500
    try:
        data = request.get_json()
        input_df = pd.DataFrame([data])
        prediction = model.predict(input_df)
        return jsonify({'prediction': int(prediction[0])})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if PORT is not set
    app.run(debug=True, host='0.0.0.0', port=port)