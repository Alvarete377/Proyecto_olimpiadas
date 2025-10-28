from django.urls import path
from . import views
from .views import EncuentrosListView

urlpatterns = [
    path("partidos/", EncuentrosListView.as_view(), name="partidos"),
]
