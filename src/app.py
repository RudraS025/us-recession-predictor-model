import os
from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))  # Path to the src directory
MODEL_PATH = os.path.join(os.path.dirname(APP_ROOT), 'models', 'vertex_model.joblib')
model = None

@app.before_first_request
def load_model():
    global model
    print("Attempting to load the model...")
    try:
        model = joblib.load(MODEL_PATH)
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        model = None

@app.route('/', methods=['GET'])
def index():
    return "US Recession Prediction API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
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