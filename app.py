from fastapi import FastAPI, Form
import uvicorn
from parameter import CropRecommendation
import numpy as np
import pandas as pd
import tensorflow as tf
import logging

# Initialize the logger
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Load the model
try:
    MODEL = tf.keras.models.load_model("Recommendation.h5")
except Exception as e:
    logging.error(f"Failed to load model: {e}")
    MODEL = None

CROP = {
    20: "rice",
    11: "maize",
    3: "chickpea",
    9: "kidneybeans",
    18: "pigeonpeas",
    13: "mothbeans",
    14: "mungbean",
    2: "blackgram",
    10: "lentil",
    19: "pomegranate",
    1: "banana",
    12: "mango",
    7: "grapes",
    21: "watermelon",
    15: "muskmelon",
    0: "apple",
    16: "orange",
    17: "papaya",
    4: "coconut",
    6: "cotton",
    8: "jute",
    5: "coffee",
}


def recommendation(N, P, k, temperature, humidity, ph, rainfal):
    try:
        features = np.array([[N, P, k, temperature, humidity, ph, rainfal]])
        prediction = MODEL.predict(features)
        return np.argmax(prediction)
    except Exception as e:
        logging.error(f"Failed to make prediction: {e}")
        return None


@app.get("/")
async def ping():
    return "Hello, It is running"


@app.post("/predict")
async def post(data: CropRecommendation):
    data = data.dict()
    logging.info(f"Received data: {data}")

    try:
        Nitrogen = float(data["nitrogen"])
        Phosporus = float(data["phosporus"])
        Potassium = float(data["potassium"])
        Temperature = float(data["temperature"])
        Humidity = float(data["humidity"])
        Ph = float(data["ph"])
        Rainfall = float(data["rainfall"])

        # Validate input values
        if (
            Nitrogen < 0
            or Phosporus < 0
            or Potassium < 0
            or Temperature < 0
            or Humidity < 0
            or Ph < 0
            or Rainfall < 0
        ):
            return {"error": "All input values must be non-negative"}

        if Ph > 15:
            return {"error": "pH must be between 0 and 15"}

        prediction = recommendation(
            Nitrogen, Phosporus, Potassium, Temperature, Humidity, Ph, Rainfall
        )

        if prediction is None:
            return {"error": "Failed to make prediction"}

        crop_name = CROP.get(prediction)

        if crop_name is None:
            return {"error": "Failed to get crop name"}

        return {"crop": crop_name}

    except Exception as e:
        logging.error(f"Failed to process request: {e}")
        return {"error": "Failed to process request"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
