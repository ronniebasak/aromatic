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
    engine = AIOAromaEngine(hosts="http://localhost:8529", database='romatic_test', username='root', password='openSesame')

    engine._map_doc_before_save(obj1)
    d = await engine.save(obj1)
    await engine.client.close()


async def main2():
    engine = AIOAromaEngine(hosts="http://localhost:8529", database='romatic_test', username='root', password='openSesame')

    d = await engine.find(MyData2)
    print(d)

    d[0].name = "HahaBaa"
    await engine.save(d[0])
    await engine.client.close()

async def main3():
    engine = AIOAromaEngine(hosts="http://localhost:8529", database='romatic_test', username='root', password='openSesame')

    d = await engine.find(MyData2)
    print(d)

    # d[0].name = "HIHIHIHI"
    dx = await engine.delete(d[0])
    print(dx)
    await engine.client.close()

loop = asyncio.run(main3())
