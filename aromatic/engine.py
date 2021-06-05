import asyncio

from aioarangodb import (ArangoClient, ArangoError, ArangoClientError, ArangoServerError)
from aioarangodb.database import Database
from aioarangodb.collection import StandardCollection as Collection
from typing import (Optional, Type, TypeVar, List)
from aromatic.basemodel import BaseAromaticModel
import aromatic.errors as errors
from pydantic import BaseModel
from pprint import pprint
from enum import Enum


class AromaticFindFallbackOptions(Enum):
    ERROR = 'ERROR'
    EMPTY_ARRAY = 'EMPTY_ARRAY'
    NONE = 'NONE'


ModelType = TypeVar("ModelType", bound=BaseAromaticModel)


class AIOAromaEngine:
    database: Database

    def __init__(self, arango_client: Optional[ArangoClient], database: str = "test", username: Optional[str] = None,
                 password: Optional[str] = None):
        if arango_client is None:
            arango_client = ArangoClient()
        self.client = arango_client
        self.database_name = database
        self.username = username
        self.password = password
        self.ready_state = "init"

    def __await__(self):
        self.database = yield from self.client.db(self.database_name, username=self.username,
                                                  password=self.password).__await__();
        self.ready_state = "db_init"
        print("READY STATE")

    def get_document_collection(self, model: Type[ModelType]) -> Collection:
        pass

    @staticmethod
    def _map_doc_before_save(document: dict) -> dict:
        if document.get('id'):
            document["_id"] = document.get("id")
        if document.get('key'):
            document["_key"] = document.get("key")
        if document.get('rev'):
            document["_rev"] = document.get("rev")

        del document['id']
        del document['rev']
        del document['key']
        return document

    async def save(self, model: Type[ModelType]) -> Type[ModelType]:
        if not self.ready_state == "db_init":
            await self
        if not model.Meta or model.Meta is None:
            raise errors.AromaticInvalidModel("The supplied model does not have valid a valid meta class")

        _collection_name: str = model.Meta.collection_name
        if await self.database.has_collection(_collection_name):
            _collection: Collection = self.database.collection(_collection_name)
        else:
            _collection: Collection = await self.database.create_collection(_collection_name)

        _doc_to_save = self._map_doc_before_save(model.dict())
        print(_doc_to_save)
        db_ack = await self.database.insert_document(_collection_name, _doc_to_save, True, True)
        model.id = db_ack['_id']
        model.key = db_ack['_key']
        model.rev = db_ack['_rev']
        return model

    async def find(self, model: ModelType, query: Optional[dict] = None,
                   fallback: AromaticFindFallbackOptions = AromaticFindFallbackOptions.EMPTY_ARRAY) -> List[
        Type[ModelType]]:
        if not self.ready_state == "db_init":
            await self

        if not model.Meta.collection_name:
            raise errors.AromaticException("Could not look up collection name for this model")

        _collection_name: str = model.Meta.collection_name
        if await self.database.has_collection(_collection_name):
            _collection: Collection = self.database.collection(_collection_name)
        else:
            if fallback == AromaticFindFallbackOptions.EMPTY_ARRAY:
                return []
            elif fallback == AromaticFindFallbackOptions.NONE:
                return None
            elif fallback == AromaticFindFallbackOptions.ERROR:
                raise errors.AromaticCollectionNotFound()

        _filter: dict = {} if type(query) != dict else query
        data: Collection = self.database.collection(_collection_name)

        _docs = await data.find(_filter)
        docs = [model(**doc) async for doc in _docs]

        if len(docs):
            return docs
        else:
            if fallback == AromaticFindFallbackOptions.EMPTY_ARRAY:
                return []
            elif fallback == AromaticFindFallbackOptions.NONE:
                return errors.AromaticCollectionNotFound()
            elif fallback == AromaticFindFallbackOptions.ERROR:
                raise errors.AromaticCollectionNotFound()

    async def find_one(self, model: ModelType, query: Optional[dict] = None,
                       fallback: AromaticFindFallbackOptions = AromaticFindFallbackOptions.EMPTY_ARRAY) -> \
            Type[ModelType]:
        if not self.ready_state == "db_init":
            await self
        if not model.Meta.collection_name:
            raise errors.AromaticException("Could not look up collection name for this model")

        _collection_name: str = model.Meta.collection_name
        if await self.database.has_collection(_collection_name):
            _collection: Collection = self.database.collection(_collection_name)
        else:
            if fallback == AromaticFindFallbackOptions.EMPTY_ARRAY:
                raise errors.AromaticCollectionNotFound()
            elif fallback == AromaticFindFallbackOptions.NONE:
                return None
            elif fallback == AromaticFindFallbackOptions.ERROR:
                raise errors.AromaticCollectionNotFound()

        _filter: dict = {} if type(query) != dict else query
        data: Collection = self.database.collection(_collection_name)

        _docs = await data.find(_filter, skip=0, limit=1)
        doc = [model(**doc) async for doc in _docs]

        if len(doc):
            return doc[0]
        else:
            if fallback == AromaticFindFallbackOptions.EMPTY_ARRAY:
                errors.AromaticCollectionNotFound()
            elif fallback == AromaticFindFallbackOptions.NONE:
                return None
            elif fallback == AromaticFindFallbackOptions.ERROR:
                raise errors.AromaticCollectionNotFound()