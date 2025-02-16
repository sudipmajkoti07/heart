from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import numpy as np
import joblib
from pydantic import BaseModel

# Define the input data model using Pydantic
class Item(BaseModel):
    Cholesterol_Level: float
    Resting_BP: float
    BMI: float
    Max_Heart_Rate_Achieved: float
    Heart_Rate: float
    Age: int

# Load the model (make sure your model file is in the correct location)
model = joblib.load('model.pkl')

# Initialize FastAPI app
app = FastAPI()

# Root route to serve HTML form
@app.get("/", response_class=HTMLResponse)
async def home():
    html_content = """
    <html>
        <head>
            <title>Heart Attack Risk Prediction</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f7f6;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }
                .container {
                    background-color: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    width: 400px;
                    text-align: center;
                }
                h2 {
                    color: #4CAF50;
                    font-size: 24px;
                    margin-bottom: 20px;
                }
                label {
                    font-size: 16px;
                    margin-top: 10px;
                    display: block;
                    text-align: left;
                }
                input[type="text"], input[type="number"] {
                    width: 100%;
                    padding: 10px;
                    margin: 10px 0;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    font-size: 14px;
                }
                button {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    font-size: 16px;
                    border-radius: 5px;
                    cursor: pointer;
                    width: 100%;
                }
                button:hover {
                    background-color: #45a049;
                }
                .result {
                    margin-top: 20px;
                    font-size: 18px;
                    font-weight: bold;
                    color: #333;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Heart Attack Risk Prediction</h2>
                <form id="inputForm">
                    <label for="cholesterol">Cholesterol Level:</label>
                    <input type="text" id="cholesterol" name="cholesterol"><br>

                    <label for="resting_bp">Resting BP:</label>
                    <input type="text" id="resting_bp" name="resting_bp"><br>

                    <label for="bmi">BMI:</label>
                    <input type="text" id="bmi" name="bmi"><br>

                    <label for="max_heart_rate">Max Heart Rate Achieved:</label>
                    <input type="text" id="max_heart_rate" name="max_heart_rate"><br>

                    <label for="heart_rate">Heart Rate:</label>
                    <input type="text" id="heart_rate" name="heart_rate"><br>

                    <label for="age">Age:</label>
                    <input type="text" id="age" name="age"><br>

                    <button type="button" onclick="submitForm()">Predict Risk</button>
                </form>

                <div class="result" id="result"></div>
            </div>

            <script>
                async function submitForm() {
                    const data = {
                        Cholesterol_Level: parseFloat(document.getElementById("cholesterol").value),
                        Resting_BP: parseFloat(document.getElementById("resting_bp").value),
                        BMI: parseFloat(document.getElementById("bmi").value),
                        Max_Heart_Rate_Achieved: parseFloat(document.getElementById("max_heart_rate").value),
                        Heart_Rate: parseFloat(document.getElementById("heart_rate").value),
                        Age: parseInt(document.getElementById("age").value)
                    };

                    const response = await fetch('/predict', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(data)
                    });

                    const result = await response.json();
                    document.getElementById("result").innerHTML = `Heart Attack Risk: ${result.Heart_Attack_Risk}`;
                }
            </script>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# Prediction route
@app.post("/predict")
async def predict(data: Item):
    # Prepare input features
    features = np.array([[ 
        data.Cholesterol_Level, 
        data.Resting_BP, 
        data.BMI, 
        data.Max_Heart_Rate_Achieved, 
        data.Heart_Rate, 
        data.Age 
    ]])

    # Make prediction
    prediction = model.predict(features)
    
    # Return result as JSON
    return {"Heart_Attack_Risk": int(prediction[0])}
