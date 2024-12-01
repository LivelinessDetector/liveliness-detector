import math
import numpy as np
import cvzone
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import cv2
import base64
from pydantic import BaseModel
import logging

# Initialize FastAPI app
app = FastAPI()

# Enable logging
logging.basicConfig(level=logging.INFO)

# CORS settings for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, adjust as needed for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the YOLO model
try:
    model = YOLO("models/n_version_2_3.pt")
except Exception as e:
    logging.error(f"Error loading YOLO model: {e}")
    raise RuntimeError("Failed to load YOLO model")

# Class names for detection
classNames = ["fake", "real"]


# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the YOLO API"}


# Input model for validation
class ImageData(BaseModel):
    image: str


@app.post("/predict/")
async def predict(data: ImageData):
    logging.info("Received request for prediction")

    # Decode the base64 image data
    try:
        img_data = base64.b64decode(data.image.split(',')[1])
        img_array = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error decoding image: {e}")

    # Run YOLO model for detection
    try:
        results = model(img, stream=True, verbose=False)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running YOLO model: {e}")

    # Process the detection results
    real_count = 0
    fake_count = 0
    for r in results:
        boxes = r.boxes
        for box in boxes:
            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])

            if classNames[cls] == "real":
                real_count += 1
            else:
                fake_count += 1

    # Return the result as a JSON response
    return JSONResponse(content={
        "success": True,
        "prediction": f"Real: {real_count}, Fake: {fake_count}"
    })