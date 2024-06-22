from pathlib import Path

import petl
import pytest

from ..utils import generate_collection_filename, save_star_wars_data


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
