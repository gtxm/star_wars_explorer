import pytest


@pytest.mark.django_db
def test_home(client):
    response = client.get("/")
    assert b"Star Wars Explorer" in response.content
