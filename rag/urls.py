from django.urls import path

from . import views

app_name = "rag"

urlpatterns = [
    path("search_on_chunks/", views.DocumentListView.as_view(), name="search-on-chunks"),
]
