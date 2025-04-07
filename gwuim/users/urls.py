from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/attendance-chart-data/', views.attendance_chart_data, name='attendance_chart_data'),
    path('api/attendance-pie-chart-data/', views.attendance_pie_chart_data, name='attendance_pie_chart_data'),
]