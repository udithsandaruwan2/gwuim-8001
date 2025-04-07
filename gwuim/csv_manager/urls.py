from django.urls import path
from . import views

urlpatterns = [
    path('import-export-manager', views.importExport, name='csv_manager'),
    # path('export-employees/', views.export_employees_csv, name='export_employees_csv'),
    path('export-attendance-pdf/', views.export_attendance_pdf, name='export_attendance_pdf'),
]