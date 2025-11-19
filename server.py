import logging

from fastapi import FastAPI

from contextlib import asynccontextmanager

from pathlib import Path

from predict_local import load_pipeline, predict


logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)

ml_model = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.debug("Starting the service")
    sklearn_pipeline_path = Path("assets/sklearn_pipeline.bin")
    ml_model["pipeline"] = load_pipeline(sklearn_pipeline_path)

    yield

    ml_model.clear()
    logger.debug("Disconnecting the service")


app = FastAPI(title="abalon-prediction", lifespan=lifespan)


@app.post("/predict")
def service_predict(
    X: dict,
):
    y_pred = predict(X["data"], ml_model["pipeline"])

    return y_pred
