import asyncio

from aioarangodb import (ArangoClient, ArangoError, ArangoClientError, ArangoServerError)
from aioarangodb.collection import Collection
from typing import (Optional, Type, TypeVar)
from aromatic.basemodel import BaseAromaticModel
import aromatic.errors as errors
from pydantic import BaseModel
from pprint import pprint

ModelType = TypeVar("ModelType", bound=BaseAromaticModel)


class AIOAromaEngine:
    def __init__(self, arango_client: Optional[ArangoClient], database: str = "test", username: Optional[str] = None, password: Optional[str] = None):
        if arango_client is None:
            arango_client = ArangoClient()
        self.client = arango_client
        self.database_name = database

        loop = asyncio.get_event_loop()
        self.database = loop.run_until_complete(self.client.db(self.database_name, username=username, password=password))

    def get_document_collection(self, model: Type[ModelType]) -> Collection:
        pass

    def save(self, model: Type[ModelType]) -> object:
        print("<Mudel Below>")
        print(model.Meta)
        if not model.Meta or model.Meta is None:
            raise errors.AromaticInvalidModel("The supplied model does not have valid a valid meta class")

        collection = model.Meta.collection_name

        print(model.dict())
        print("ENDDD")
