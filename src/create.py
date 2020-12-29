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

from config import DB_CONNECTION_STRING
from config import PHARMACY_API_URL

from orms import DrugsTable


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
