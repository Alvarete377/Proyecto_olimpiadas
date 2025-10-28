from django.urls import path
from . import views
from .views import EncuentrosListView, EncuentrosDetailView
urlpatterns = [
    path("partidos/", EncuentrosListView.as_view(), name="partidos"),
    path("detalles/<int:pk>/", EncuentrosDetailView.as_view(), name="detalles")
]
