import pytest
from aromatic.basemodel import BaseAromaticModel
from aromatic.engine import AIOAromaEngine
from pydantic import constr, EmailStr
from pydantic import ValidationError
from datetime import datetime
from typing import List, Tuple


@pytest.mark.asyncio
async def test_create(engine: AIOAromaEngine):
    """Testing saving a model and getting the same model"""

    class MyClass(BaseAromaticModel):
        username: str
        password: str

        class Meta:
            collection_name: str = "test_crud_1"

    obj = MyClass(username="bojack", password="horseman")
    d1 = obj.dict()

    saved: MyClass = await engine.save(obj)
    assert type(saved.id) == str
    assert type(saved.key) == str
    assert type(saved.rev) == str
    assert saved.id != "" and saved.key != "" and saved.rev != ""

    d2 = saved.dict()
    del d2['id']
    del d2['rev']
    del d2['key']
    del d1['id']
    del d1['rev']
    del d1['key']

    assert d1 == d2


@pytest.mark.asyncio
async def test_read(engine: AIOAromaEngine):
    """Testing saving a model and getting the same model"""

    class MyClass(BaseAromaticModel):
        username: str
        password: str

        class Meta:
            collection_name: str = "test_crud_1"

    found: MyClass = await engine.find_one(MyClass, {'username': 'bojack'})
    assert found is not None
    assert found.username == "bojack"
    assert found.password == "horseman"
    assert found.id != "" and found.rev != "" and found.key != ""


@pytest.mark.asyncio
async def test_update(engine: AIOAromaEngine):
    """Testing saving a model and getting the same model"""

    class MyClass(BaseAromaticModel):
        username: str
        password: str

        class Meta:
            collection_name: str = "test_crud_1"

    found: MyClass = await engine.find_one(MyClass, {'username': 'bojack'})
    found.username = "mewmew"
    obj1 = found.dict()

    saved: MyClass = await engine.save(found)
    obj2 = saved.dict()

    assert obj1['id'] == obj2['id'], "Separate id, failed to update"
    assert obj1['rev'] != obj2['rev'], "Same revision, no change has occurred"
    assert saved.username == "mewmew", "Value did not update successfully"
    assert saved.password == "horseman", "Old value did not persist the update"
