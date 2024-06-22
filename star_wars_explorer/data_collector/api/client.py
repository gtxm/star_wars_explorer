from django.conf import settings
from requests import Session


class StarWarsAPIClient:

    def __init__(self):
        self.session = Session()

    def handle_pagination(self, first_url):
        response = self.session.get(first_url)
        yield from response.json()["results"]
        next_page = response.json().get("next", None)
        while next_page:
            response = self.session.get(next_page)
            yield from response.json()["results"]
            next_page = response.json().get("next", None)

    def get_people(self):
        # TODO proper error handling
        yield from self.handle_pagination(
            settings.DATA_COLLECTOR_API_BASE_URL + "api/people/?format=json"
        )

    def get_planets(self):
        yield from self.handle_pagination(
            settings.DATA_COLLECTOR_API_BASE_URL + "api/planets/?format=json"
        )
