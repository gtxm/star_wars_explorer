from django.urls import path

from . import views


urlpatterns = [path("", views.home), path("fetch", views.fetch), path("details/<int:pk>/", views.details)]
