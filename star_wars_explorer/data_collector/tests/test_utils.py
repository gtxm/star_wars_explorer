from pathlib import Path
from unittest.mock import patch, Mock

import petl
import pytest

from ..utils import (
    generate_collection_filename,
    save_star_wars_data,
    transform_collected_data,
    fetch_latest_dataset,
)


def test_generate_collection_filename():
    filename = generate_collection_filename()
    assert filename.split(".")[1] == "csv"


@pytest.mark.django_db
def test_save_star_wars_data():
    sample_data = petl.wrap(
        [
            (
                "test",
                1,
            )
        ]
    )
    collection = save_star_wars_data(sample_data)

    assert ".csv" in collection.filename
    assert Path(collection.full_path).exists()
    assert list(petl.fromcsv(collection.full_path)) == [
        (
            "test",
            "1",
        )
    ]

    # cleanup
    Path(collection.full_path).unlink()


def test_transform_collected_data():
    planet_resource_uri_to_name = {"https://swapi.dev/api/planets/1/": "Tatooine"}
    data = petl.fromdicts(
        [
            {
                "name": "Anakin Skywalker",
                "height": "188",
                "mass": "84",
                "hair_color": "blond",
                "skin_color": "fair",
                "eye_color": "blue",
                "birth_year": "41.9BBY",
                "gender": "male",
                "homeworld": "https://swapi.dev/api/planets/1/",
                "films": [
                    "https://swapi.dev/api/films/4/",
                    "https://swapi.dev/api/films/5/",
                    "https://swapi.dev/api/films/6/",
                ],
                "species": [],
                "vehicles": [
                    "https://swapi.dev/api/vehicles/44/",
                    "https://swapi.dev/api/vehicles/46/",
                ],
                "starships": [
                    "https://swapi.dev/api/starships/39/",
                    "https://swapi.dev/api/starships/59/",
                    "https://swapi.dev/api/starships/65/",
                ],
                "created": "2014-12-10T16:20:44.310000Z",
                "edited": "2014-12-20T21:17:50.327000Z",
                "url": "https://swapi.dev/api/people/11/",
            }
        ]
    )
    transformed_data = transform_collected_data(data, planet_resource_uri_to_name)
    assert transformed_data.header() == (
        "name",
        "height",
        "mass",
        "hair_color",
        "skin_color",
        "eye_color",
        "birth_year",
        "gender",
        "homeworld",
        "date",
    )
    assert list(transformed_data.values("homeworld")) == [
        "Tatooine",
    ]


@pytest.mark.django_db
def test_fetch_latest_dataset():
    mock_client = Mock()
    mock_client.get_planets.return_value = [
        {
            "name": "Tatooine",
            "rotation_period": "23",
            "orbital_period": "304",
            "diameter": "10465",
            "climate": "arid",
            "gravity": "1 standard",
            "terrain": "desert",
            "surface_water": "1",
            "population": "200000",
            "residents": [
                "https://swapi.dev/api/people/1/",
                "https://swapi.dev/api/people/2/",
                "https://swapi.dev/api/people/4/",
                "https://swapi.dev/api/people/6/",
                "https://swapi.dev/api/people/7/",
                "https://swapi.dev/api/people/8/",
                "https://swapi.dev/api/people/9/",
                "https://swapi.dev/api/people/11/",
                "https://swapi.dev/api/people/43/",
                "https://swapi.dev/api/people/62/",
            ],
            "films": [
                "https://swapi.dev/api/films/1/",
                "https://swapi.dev/api/films/3/",
                "https://swapi.dev/api/films/4/",
                "https://swapi.dev/api/films/5/",
                "https://swapi.dev/api/films/6/",
            ],
            "created": "2014-12-09T13:50:49.641000Z",
            "edited": "2014-12-20T20:58:18.411000Z",
            "url": "https://swapi.dev/api/planets/1/",
        },
    ]
    mock_client.get_people.return_value = [
        {
            "name": "Luke Skywalker",
            "height": "172",
            "mass": "77",
            "hair_color": "blond",
            "skin_color": "fair",
            "eye_color": "blue",
            "birth_year": "19BBY",
            "gender": "male",
            "homeworld": "https://swapi.dev/api/planets/1/",
            "films": [
                "https://swapi.dev/api/films/1/",
                "https://swapi.dev/api/films/2/",
                "https://swapi.dev/api/films/3/",
                "https://swapi.dev/api/films/6/",
            ],
            "species": [],
            "vehicles": [
                "https://swapi.dev/api/vehicles/14/",
                "https://swapi.dev/api/vehicles/30/",
            ],
            "starships": [
                "https://swapi.dev/api/starships/12/",
                "https://swapi.dev/api/starships/22/",
            ],
            "created": "2014-12-09T13:50:51.644000Z",
            "edited": "2014-12-20T21:17:56.891000Z",
            "url": "https://swapi.dev/api/people/1/",
        }
    ]
    with patch("data_collector.utils.StarWarsAPIClient", return_value=mock_client):
        collection = fetch_latest_dataset()

    assert list(petl.fromcsv(collection.full_path).dicts()) == [
        {
            "name": "Luke Skywalker",
            "height": "172",
            "mass": "77",
            "hair_color": "blond",
            "skin_color": "fair",
            "eye_color": "blue",
            "birth_year": "19BBY",
            "gender": "male",
            "homeworld": "Tatooine",
            "date": "2014-12-20",
        }
    ]
