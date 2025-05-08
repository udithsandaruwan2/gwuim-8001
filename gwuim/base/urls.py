from django.urls import path
from . import views

urlpatterns = [
    path("", views.getRoutes, name="api"),
    path("vacations/", views.getVacationDetails, name="api_vacations"),

]