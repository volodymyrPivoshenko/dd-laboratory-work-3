"""
API for DB.
"""

import uvicorn

import pandas as pd

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from orms import DrugsTable
from orms import DrugModel
from orms import DrugsModel
from orms import InputModel


DB_CONNECTION_STRING = (
    "postgres://cqnphkrqcerybi:6ee5b724c28ce16392ea860bf8a2c63fd3456555f34780ca6e775f1c9f7ab880@ec2-34-253-148-186.eu-west-1.compute.amazonaws.com:5432/d84lht7ldah19p"
)

# create connection
ENGINE = create_engine(DB_CONNECTION_STRING)
BASE = declarative_base()

app = FastAPI()


@app.get("/healthcheck", status_code=200)
async def healthcheck():
    """
    Index page.
    """

    return "Everything is ok!"


@app.post("/drug", response_model=DrugModel)
async def getDrug(drug: InputModel):
    """
    Get drug.
    """

    session = sessionmaker(ENGINE)()
    BASE.metadata.create_all(ENGINE)

    response = session.query(DrugsTable).filter(DrugsTable.code == drug.code)[0]

    return DrugModel(
        code=response.code or 0,
        barcode=response.barcode or 0,
        name=response.name or 0,
        producer=response.producer or 0,
        tax=response.tax or 0,
        price=response.price or 0,
        quantity=response.quantity or 0,
        price_reserve=response.price_reserve or 0,
        price_reserve_order=response.price_reserve_order or 0,
    )


@app.post("/all", response_model=DrugsModel)
async def getAll():
    """
    Get all drugs.
    """

    session = sessionmaker(ENGINE)()
    BASE.metadata.create_all(ENGINE)

    responses = session.query(DrugsTable)

    return DrugsModel(
        drugs=list(
            DrugModel(
                code=response.code or 0,
                barcode=response.barcode or 0,
                name=response.name or 0,
                producer=response.producer or 0,
                tax=response.tax or 0,
                price=response.price or 0,
                quantity=response.quantity or 0,
                price_reserve=response.price_reserve or 0,
                price_reserve_order=response.price_reserve_order or 0,
            )
            for response in responses
        )
    )


if __name__ == "__main__":
    """
    Entrypoint.
    """

    uvicorn.run(app, host="0.0.0.0", port=8000)
