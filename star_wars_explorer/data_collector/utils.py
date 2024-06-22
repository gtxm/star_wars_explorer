import uuid

import petl

from .models import StarWarsDataCollection


def generate_collection_filename():
    return f"{uuid.uuid4().hex}.csv"


def save_star_wars_data(data: petl.Table):
    collection = StarWarsDataCollection.objects.create(
        filename=generate_collection_filename()
    )
    collection.save_data(data)
    return collection
