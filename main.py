from fastapi import FastAPI
import pandas as pd
from sklearn.linear_model import LinearRegression

app = FastAPI()

# Dummy model
model = LinearRegression()

@app.get("/")
def home():
    return {"message": "House price API running"}

@app.post("/predict")
def predict(size: float):
    price = size * 1000  # fake logic
    return {"predicted_price": price}
