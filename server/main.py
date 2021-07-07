import os
import pandas as pd
import uvicorn
from fastapi import FastAPI, datastructures

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(BASE_DIR, 'cache')
dataset = os.path.join(CACHE_DIR, 'movies_dataset_cleaned.csv')
app = FastAPI()


@app.get('/')
def read_root():
    return {"Hello": "World"}


@app.get("/box-office")
def read_box_office_numbers():
    df = pd.read_csv(dataset)
    return df.to_dict("Rank")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        reload=False,
        port=8000,
    )
