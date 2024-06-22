from django.conf import settings
from requests import Session


class StarWarsAPIClient:

    def __init__(self):
        self.session = Session()

    def get_people(self):
        # TODO proper error handling
        response = self.session.get(
            settings.DATA_COLLECTOR_API_BASE_URL + "api/people/?format=json"
        )
        yield from response.json()["results"]
        next_page = response.json().get("next", None)
        while next_page:
            response = self.session.get(next_page)
            yield from response.json()["results"]
            next_page = response.json().get("next", None)
