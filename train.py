import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import mlflow
import mlflow.sklearn
import joblib  # Added for local saving
import os      # Added to ensure directory exists

# load data
data = pd.read_csv("data/data.csv")

X = data.iloc[:, :-1]
y = data.iloc[:, -1]

model = LinearRegression()

with mlflow.start_run():
    model.fit(X, y)
    preds = model.predict(X)

    mae = mean_absolute_error(y, preds)
    rmse = mean_squared_error(y, preds) ** 0.5

    mlflow.log_metric("MAE", mae)
    mlflow.log_metric("RMSE", rmse)

    mlflow.sklearn.log_model(model, "model")

    # --- LOCAL SAVING LOGIC FOR TASK 3 ---
    # Ensure the 'api' folder exists as per your folder structure
    if not os.path.exists("api"):
        os.makedirs("api")
    
    # Save the model as model.pkl inside the api/ directory
    joblib.dump(model, "api/model.pkl")

print("Training complete and model.pkl saved locally in api/")