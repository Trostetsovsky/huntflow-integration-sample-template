from reprlib import Repr

import pytest
from httpx import AsyncClient
from hf_integration_sample.app.fastapi import create_app

my_repr = Repr()
my_repr.maxstring = 50


def pytest_make_parametrize_id(config, val):
    return my_repr.repr(val)


@pytest.fixture
async def client():
    async with AsyncClient(app=create_app(), base_url="http://testserver") as client:
        yield client


@pytest.fixture
def non_mocked_hosts() -> list:
    return ["testserver"]
