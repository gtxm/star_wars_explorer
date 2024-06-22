import responses

from data_collector.api.client import StarWarsAPIClient


class TestStarWarsAPIClient:

    @responses.activate
    def test_get_people(self):
        responses.add(
            "GET",
            "https://swapi.dev/api/people/?format=json",
            json={
                "count": 2,
                "next": "https://swapi.dev/api/people/?page=2&format=json",
                "previous": None,
                "results": [
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
                    },
                ],
            },
        )
        responses.add(
            "GET",
            "https://swapi.dev/api/people/?page=2&format=json",
            json={
                "count": 2,
                "next": None,
                "previous": "https://swapi.dev/api/people/?format=json",
                "results": [
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
                ],
            },
        )
        client = StarWarsAPIClient()
        assert [person["name"] for person in client.get_people()] == [
            "Luke Skywalker",
            "Anakin Skywalker",
        ]
