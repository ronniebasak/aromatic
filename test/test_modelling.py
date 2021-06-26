import pytest
from aromatic.basemodel import BaseAromaticModel
from aromatic.engine import AIOAromaEngine
from pydantic import BaseModel, constr, EmailStr, ValidationError
from datetime import datetime, timezone, timedelta
from typing import List, Tuple


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


@pytest.mark.asyncio
async def test_modelling_2(engine: AIOAromaEngine):
    """Testing saving a model and getting the same model"""

    class MyClass(BaseAromaticModel):
        username: str
        password: constr(min_length=6, max_length=32)
        email: EmailStr
        rank: int
        created: datetime
        tupp: Tuple[str, int, int]
        liss: List[str]

        class Meta:
            collection_name: str = "test_124"

    try:
        MyClass(username="asd", password="12345", email= "random@example.com", rank=34, created=datetime.utcnow(), tupp= ("asd",1,1), liss=["asd","asdasd"])
    except Exception as e:
        err = e
    assert 'err' in dir(), "validation did not fail"
    assert type(err) == ValidationError

    try:
        MyClass(username="asd", password="123456", email= "random", rank=34, created=datetime.utcnow(), tupp= ("asd",1,1), liss=["asd","asdasd"])
    except Exception as e:
        err = e
    assert 'err' in dir(), "validation did not fail"
    assert type(err) == ValidationError

    try:
        MyClass(username="asd", password="123456", email= "random@example.com", rank="@@34", created=datetime.utcnow(), tupp= ("asd",1,1), liss=["asd","asdasd"])
    except Exception as e:
        err = e
    assert 'err' in dir(), "validation did not fail"
    assert type(err) == ValidationError

    try:
        MyClass(username="asd", password="123456", email= "random@example.com", rank=4, created="WOW", tupp= ("asd",1,1), liss=["asd","asdasd"])
    except Exception as e:
        err = e
    assert 'err' in dir(), "validation did not fail"
    assert type(err) == ValidationError

    try:
        MyClass(username="asd", password="123456", email= "random@example.com", rank=4, created=datetime.utcnow(), tupp= (2,"s",1), liss=["asd","asdasd"])
    except Exception as e:
        err = e
    assert 'err' in dir(), "validation did not fail"
    assert type(err) == ValidationError

    try:
        MyClass(username="asd", password="123456", email= "random@example.com", rank=4, created=datetime.utcnow(), tupp= (2,1,1), liss=[33,44, {1}])
    except Exception as e:
        err = e
    assert 'err' in dir(), "validation did not fail"
    assert type(err) == ValidationError

    try:
        obj = MyClass(username="asd", password="123456", email= "random@example.com", rank=4, created=datetime.utcnow(), tupp= (2,1,1), liss=["asd"])
    except Exception as e:
        err2 = e
    assert 'err2' not in dir(), "validation failed"
    d1 = obj.dict()
    obj2 = await engine.save(obj)
    d2 = obj2.dict()
    assert obj2.id != "" and obj2.rev != "" and obj2.key != ""
    del d1['id']
    del d1['rev']
    del d1['key']
    del d2['id']
    del d2['rev']
    del d2['key']
    assert d1 == d2


@pytest.mark.asyncio
async def test_modelling_3(engine: AIOAromaEngine):
    """Testing saving Embedded Model"""

    class Profile(BaseModel):
        email: EmailStr

    class MyClass(BaseAromaticModel):
        username: str
        password: str
        profile: Profile

        class Meta:
            collection_name: str = "test_123"

    obj = MyClass(username="unique_todd", password="horseman", profile=Profile(email="abc@example.com"))
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

    obj2 = await engine.find_one(MyClass, {'username': 'unique_todd'})
    assert saved.dict() == obj2.dict()
    assert obj2.profile.email == "abc@example.com"\


@pytest.mark.asyncio
async def test_datetime(engine: AIOAromaEngine):
    """Testing saving and finding non-naive datetime"""
    import pytz

    class MyClass(BaseAromaticModel):
        username: str
        password: str
        SED: datetime

        class Meta:
            collection_name: str = "test_123"

    obj = MyClass(username="unique_mahi", password="horseman", SED=datetime.fromisoformat("2020-01-01T00:00+05:30"))
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

    obj2 = await engine.find_one(MyClass, {'username': 'unique_mahi'})
    assert saved.dict() == obj2.dict()
    assert obj2.SED.tzinfo == timezone(timedelta(seconds=19800))