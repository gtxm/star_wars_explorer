from pathlib import Path

import petl
import pytest

from ..utils import (
    generate_collection_filename,
    save_star_wars_data,
    transform_collected_data,
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
    transformed_data = transform_collected_data(data)
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
