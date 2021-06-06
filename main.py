# from pydantic import BaseModel
# from typing import Optional
# from pprint import pprint
import asyncio
from datetime import datetime, date
from typing import List, Tuple

from aioarangodb import ArangoClient

from aromatic import basemodel
from aromatic.engine import AIOAromaEngine


class MyData2(basemodel.BaseAromaticModel):
    name: str
    num: int
    list: List[int]
    tup: Tuple[str, int]
    ts: datetime
    dt: date

    class Meta:
        collection_name: str = "arango2_col"


async def main():
    obj1 = MyData2(name="Sohan", num=2, list=[2, 3, 4], tup=("S", 2), ts=datetime.utcnow(), dt=date.today())
    print(obj1)
    client = ArangoClient()
    engine = AIOAromaEngine(arango_client=client, database='romatic_test', username='root', password='openSesame')

    engine._map_doc_before_save(obj1)
    d = await engine.save(obj1)
    await client.close()


async def main2():
    client = ArangoClient()
    engine = AIOAromaEngine(arango_client=client, database='romatic_test', username='root', password='openSesame')

    d = await engine.find(MyData2)
    print(d)
    await client.close()


loop = asyncio.run(main2())
