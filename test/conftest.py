# Pytest configurations go here
import asyncio
import pytest
from aromatic.engine import AIOAromaEngine

HOSTS = "http://localhost:8529"
USERNAME = "root"
PASSWORD = "openSesame"
DATABASE = "romatic_test"


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
@pytest.fixture(scope="session", autouse=True)
async def engine():
    engine = AIOAromaEngine(hosts=HOSTS, database=DATABASE, username=USERNAME, password=PASSWORD)
    await engine
    yield engine

    # COMMENT THIS LINE IF YOU WANT TO SEE THE TEST DATA PERSIST IN DATABASE
    # Also delete if you are insane
    await engine.database.delete_collection('test_123', ignore_missing=True)
    await engine.client.close()

