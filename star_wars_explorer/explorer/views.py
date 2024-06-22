from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from data_collector.models import StarWarsDataCollection
from data_collector.utils import fetch_latest_dataset


def home(request):
    return render(
        request,
        "collections.html",
        {"collections": StarWarsDataCollection.objects.order_by("-created").all()},
    )


def fetch(request):
    fetch_latest_dataset()
    return redirect("/")


def details(request, pk):
    collection = get_object_or_404(StarWarsDataCollection, pk=pk)
    table = collection.open_data().head(10)
    return render(
        request,
        "details.html",
        {"headers": table.header(), "rows": table.data(), "collection": collection},
    )
