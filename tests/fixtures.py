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

    # Note that we do this for tests, when each DB is created from scratch, but we don't do it for prod, when the
    # DB is incrementally updated via alembic
    db.create_all()

    with app.test_client() as client:
        yield client, db, app

    print('Removing Test DB')
    try:
        os.remove(TestConfig.db_filepath)  # this is teardown
    except FileNotFoundError:
        Warning('Did not manage to tear down test DB, hope this was a temporary env')


@pytest.fixture(scope='module')
def location_dict():
    loc_dict = dict(longitude=-73.5673,
                    latitude=45.5017,
                    postcode='H2S 3C3')

    yield loc_dict


@pytest.fixture(scope="session")
def test_db(setup_test_app):
    _, db, _ = setup_test_app

    yield db


@pytest.fixture(scope="session")
def test_client(setup_test_app):
    client, _, _ = setup_test_app

    yield client


@pytest.fixture(scope="session")
def test_app(setup_test_app):
    _, _, app = setup_test_app

    yield app


@pytest.fixture(scope='session')
def example_forecast():
    pass


@dataclass
class MockLocation:
    place: str
    country: str
    city: str
    lon: float
    lat: float


test_locations = [MockLocation(place='Redland, Bristol, UK',
                               city='Bristol',
                               country='England',
                               lat=51.45,
                               lon=-2.58),
                  MockLocation(place='Montreal, QC, Canada',
                               city='Montreal',
                               country='Canada',
                               lat=45.5,
                               lon=-73.6)]
