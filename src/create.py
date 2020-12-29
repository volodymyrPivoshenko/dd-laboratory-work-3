"""
Create table and fill it.
"""

import stringcase
import requests

from typing import List
from typing import Dict
from typing import Any
from xml.etree import ElementTree
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from orms import DrugsTable


DB_CONNECTION_STRING = (
    "postgres://cqnphkrqcerybi:6ee5b724c28ce16392ea860bf8a2c63fd3456555f34780ca6e775f1c9f7ab880@ec2-34-253-148-186.eu-west-1.compute.amazonaws.com:5432/d84lht7ldah19p"
)
PHARMACY_API_URL = "https://tabletki.ua/_assets/desktop/docs/pricelist/pricelist.xml"

# create connection
ENGINE = create_engine(DB_CONNECTION_STRING)
BASE = declarative_base()


def main() -> bool:
    """
    Entrypoint.
    """

    response = ElementTree.fromstring(requests.get(PHARMACY_API_URL).content)
    drugs = list(sample.attrib for sample in response)

    # parse drugs
    parsed_drugs = []
    for index, product in enumerate(drugs):
        product["code"] = str(index)
        parsed_drugs.append(
            {
                stringcase.snakecase(key): float(value) if value.isnumeric() else value
                for key, value in product.items()
                if stringcase.snakecase(key) in DrugsTable.__dict__
            }
        )
    

    # fill table
    session = sessionmaker(ENGINE)()
    BASE.metadata.create_all(ENGINE)

    for drug in parsed_drugs:
        drug = DrugsTable(**drug)
        session.add(drug)
        session.commit()

    return True


if __name__ == "__main__":
    main()
