import os
from dataclasses import dataclass

import pytest
from app_factory import create_app
from models import db
from config import TestConfig


@pytest.fixture(scope='session')
def setup_test_app():

    app = create_app(config=TestConfig)
    app.app_context().push()

    with app.test_client() as client:
        yield client, db

    print('Removing Test DB')
    os.remove(TestConfig.db_filepath)  # this is teardown


@pytest.fixture(scope='module')
def location_dict():
    loc_dict = dict(longitude=-73.5673,
                    latitude=45.5017,
                    postcode='H2S 3C3')

    yield loc_dict


@pytest.fixture(scope="session")
def test_db(setup_test_app):
    _, db = setup_test_app

    yield db


@pytest.fixture(scope="session")
def test_client(setup_test_app):
    client, _ = setup_test_app

    yield client


@pytest.fixture(scope='session')
def example_forecast():
    pass


@dataclass
class TestLocation:
    place: str
    city: str
    lon: float
    lat: float


test_locations = [TestLocation(place='BS6 7ER',
                               city='Bristol',
                               lat=51.45,
                               lon=-2.58),
                  TestLocation(place='H2S 3C2',
                               city='Montreal',
                               lat=45.5,
                               lon=-73.6)]
