import petl
from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404

from data_collector.models import StarWarsDataCollection
from data_collector.utils import fetch_latest_dataset
from explorer.utils import compute_selected_fields_after_clicking_field_button


# TODO test logic in views


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
    current_page = int(request.GET.get("page", 1))
    collection = get_object_or_404(StarWarsDataCollection, pk=pk)
    table = collection.open_data().head(
        current_page * settings.EXPLORER_ROWS_PER_PAGE
    )  # TODO handle missing file
    return render(
        request,
        "details.html",
        {
            "headers": table.header(),
            "rows": table.data(),
            "collection": collection,
            "next_page": current_page + 1,
        },
    )  # TODO handle case when there is no more data to load


def value_count(request, pk):
    selected_fields = request.GET.get("fields", "").split(",")
    if not selected_fields:
        raise Http404()
    collection = get_object_or_404(StarWarsDataCollection, pk=pk)

    table = collection.open_data()

    possible_options = [
        {
            "value": field,
            "selected": field in selected_fields,
            "fields_for_button": compute_selected_fields_after_clicking_field_button(
                field, selected_fields
            ),
        }
        for field in petl.fieldnames(table)
    ]

    table = table.aggregate(selected_fields, len)
    return render(
        request,
        "value_count.html",
        {
            "headers": table.header(),
            "rows": table.data(),
            "collection": collection,
            "possible_options": possible_options,
        },
    )
