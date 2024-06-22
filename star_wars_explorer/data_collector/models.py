import petl
from django.conf import settings
from django.db import models


class StarWarsDataCollection(models.Model):
    filename = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    @property
    def full_path(self):
        return settings.DATA_COLLECTOR_BASE_DIR + "/" + self.filename

    def save_data(self, data: petl.Table):
        data.tocsv(self.full_path)
