import uuid
import joblib
import pandas as pd
from typing import List, Dict
from pydantic import BaseModel, field_validator
from fastapi import FastAPI, BackgroundTasks, HTTPException
from src.titanic.data_processing import feature_engineering, encode_features


app = FastAPI(title="Titanic API")

model_lgbm = joblib.load("models/model.joblib")


@app.get("/")
def checking_status():
        return {"message": "OK", "docs": "API documentation inside /docs"}


class PassengerData(BaseModel): # using pydantic to validate input types of data according to https://pydantic-docs.readthedocs.io/en/stable/
    Pclass: int
    Sex: str
    Age: float
    SibSp: int
    Fare: float
    Embarked: str

    @field_validator("Pclass")
    def pclass_range(cls, val):
        if val not in [1, 2, 3]:
            raise ValueError("Pclass must be 1, 2, or 3")
        return val

    @field_validator("Age", "Fare")
    def non_negative(cls, val):
        if val < 0:
            raise ValueError("Age and Fare must be non-negative")
        return val

class PassengerDataList(BaseModel):
    data: List[PassengerData]


def process_prediction(data_dicts: List[dict]) -> List[Dict]:
    """
    Helper function to apply data-processing steps and run model inference.
    """
    df = pd.DataFrame(data_dicts) # convert to df
    df = feature_engineering(df) # extract features
    df = encode_features(df) # encoding

    preds = model_lgbm.predict(df)
    probs = model_lgbm.predict_proba(df)[:, 1]

    results = []
    for pred, prob in zip(preds, probs):
        results.append({"prediction": int(pred), "probability": float(prob)})
    return results

@app.post("/titanic_sync")
def predict_sync(input_data: PassengerDataList):
    """
    Synchronous endpoint: returns inference results immediately.
    """
    data_dicts = [item.model_dump() for item in input_data.data]
    results = process_prediction(data_dicts)
    return {"results": results}


jobs = {} # in this case I want to use simple memory storage mechanism instead of relying on sqlalchemy or redis

def backg_inference(job_id: str, data_dicts: List[dict]):
    """
    Runs inference in the background. Stores results in the global `jobs` dictionary.
    """
    try:
        output = process_prediction(data_dicts)
        jobs[job_id] = {"status": "Completed", "results": output}
    except Exception as e:
        jobs[job_id] = {"status": "Error", "error": str(e)}


@app.post("/titanic_async")
def predict_async(input_data: PassengerDataList, background_tasks: BackgroundTasks):
    """
    Asynchronous endpoint: returns a job_id, processes inference in background.
    """
    job_id = str(uuid.uuid4()) #  https://docs.python.org/3/library/uuid.html
    jobs[job_id] = None

    data_dicts = [item.model_dump() for item in input_data.data]
    background_tasks.add_task(backg_inference, job_id, data_dicts)

    return {"job_id": job_id, "status": "PENDING"}


@app.get("/titanic_async/{job_id}")
def get_async_result(job_id: str):
    """
    Check the status of an async job, retrieve the result if complete.
    """
    if job_id not in jobs:
        raise HTTPException(status_code = 404, detail = "job not found")

    job_info = jobs[job_id]
    if job_info is None:
        return {"job_id": job_id, "status": "Pending"} # stage if the job is running

    if job_info.get("status") == "Completed": # check completed
        return {"job_id": job_id,"status": "Completed", "results": job_info["results"]}

    elif job_info.get("status") == "Error": # to hangle if there is some error
        return {"job_id": job_id,"status": "Error", "error": job_info["error"]}

    return {"job_id": job_id, "status": "unknown"}


# to run in main dir: uv run python -m uvicorn src.api.main_api:app --reload --host 0.0.0.0 --port 8090
