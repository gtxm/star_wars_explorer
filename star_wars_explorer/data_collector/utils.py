import uuid

import petl

from .api.client import StarWarsAPIClient
from .models import StarWarsDataCollection


def generate_collection_filename():
    return f"{uuid.uuid4().hex}.csv"


def save_star_wars_data(data: petl.Table):
    collection = StarWarsDataCollection.objects.create(
        filename=generate_collection_filename()
    )
    collection.save_data(data)
    return collection


def transform_collected_data(data: petl.Table):
    return data.addfield("date", lambda rec: rec["edited"][:10]).cutout(
        "films", "species", "vehicles", "starships", "url", "created", "edited"
    )
