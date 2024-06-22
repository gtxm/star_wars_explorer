from django.http import HttpResponse
from django.shortcuts import render, redirect

from data_collector.models import StarWarsDataCollection
from data_collector.utils import fetch_latest_dataset


def home(request):
    return render(request, "index.html", {"collections": StarWarsDataCollection.objects.order_by("-created").all()})


def fetch(request):
    fetch_latest_dataset()
    return redirect("/")
