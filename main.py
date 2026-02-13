from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import joblib
from email_alert import send_alert

app = FastAPI()

# ---- GLOBAL VALIDATION ERROR HANDLER ----
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    send_alert(f"Validation error: {exc}")
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


# ---- LOAD MODEL ----
try:
    model = joblib.load("api/model.pkl")
except Exception as e:
    send_alert(f"Model loading failed: {e}")
    model = None


class InputData(BaseModel):
    size: float


@app.post("/predict")
def predict(data: InputData):
    try:
        if model is None:
            raise Exception("Model not loaded")

        pred = model.predict([[data.size]])
        return {"prediction": float(pred[0])}

    except Exception as e:
        send_alert(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Prediction error")
