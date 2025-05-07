from django.urls import path
from . import views

urlpatterns = [
    path("vacations/", views.vacations, name="vacations"),
    path("vacations/<int:year>/<int:month>/", views.vacations, name="vacations_month"),
]
