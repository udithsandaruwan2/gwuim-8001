from django.urls import path
from . import views
urlpatterns = [
    path('time-management/', views.timeManagement, name='time_management'),
    path('time-management/add/', views.timeManagementAdd, name='time_management_add'),
    path('time-management/<uuid:pk>/', views.timeManagementUpdate, name='time_management_update'),
    path('time-management/delete/<uuid:pk>/', views.timeManagementDelete, name='time_management_delete'),
]