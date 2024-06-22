from django.http import HttpResponse
from django.shortcuts import render

from data_collector.models import StarWarsDataCollection


def home(request):
    return render(request, "index.html", {"collections": StarWarsDataCollection.objects.all()})
