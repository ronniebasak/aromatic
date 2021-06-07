import pytest
from aromatic.basemodel import BaseAromaticModel
from aromatic.engine import AIOAromaEngine


@pytest.mark.asyncio
async def test_modelling(engine: AIOAromaEngine):
    """Testing saving a model and getting the same model"""

    class MyClass(BaseAromaticModel):
        username: str
        password: str

        class Meta:
            collection_name: str = "test_123"

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
