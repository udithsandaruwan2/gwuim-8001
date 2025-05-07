from django.urls import path
from . import views

urlpatterns = [
    path('vacations/', views.vacations, name='vacations' ),

]