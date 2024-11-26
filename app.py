from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# Step 3: Load the trained model
model = joblib.load("linear_model.pkl")

# Step 4: Initialize FastAPI app
app = FastAPI()

# Step 5: Define the input structure
class PredictionRequest(BaseModel):
    Exam_1: float
    Exam_2: float
    Exam_3: float
    Exam_4: float
    Exam_5: float
    Exam_6: float
    Attendance:float
    Study_Hours:float
    Activity_Hours: float
    Stress_Level: float
    Study_to_Activity_Ratio: float

# Step 6: Create the predict endpoint
@app.post("/predict")
def predict(request: PredictionRequest):
    try:
        # Step 7: Convert the input data to a DataFrame
        input_data = pd.DataFrame([request.dict()])
        
        # Step 8: Make predictions using the loaded model
        prediction = (model.predict(input_data) /10)
        
        # Step 9: Return the prediction as a JSON response
        return {"prediction": prediction.tolist()}
    except Exception as e:
        return {"error": str(e)}
