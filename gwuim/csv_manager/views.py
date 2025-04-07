from django.shortcuts import render, redirect
from .forms import AttendanceFileForm
from .utils import process_attendance_csv
from attendance_management.models import Attendance
import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from weasyprint import HTML
from attendance_management.models import Attendance

@login_required(login_url='login')
def importExport(request):
    page = 'csv_manager'
    page_title = 'CSV Manager'

    try:
        profile = request.user.profile
    except:
        profile = None

    if request.method == 'POST' and request.FILES:
        form = AttendanceFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the form (which saves the file)
            file_path = form.instance.file.url  # Get the relative file URL
            process_attendance_csv(file_path)  # Process the CSV file
            messages.success(request, 'File imported successfully!')
            return redirect('csv_manager')  # Redirect to 'csv_manager' page after saving
        else:
            messages.error(request, 'Invalid form submission. Please try again.')
    else:
        form = AttendanceFileForm()  # Initialize the form for GET request
        

    context = {
        'page': page,
        'page_title': page_title,
        'form': form,
        'profile': profile,
    }

    return render(request, 'csv_manager/import-export.html', context)

# views.py



def export_attendance_pdf(request):
    attendance = Attendance.objects.filter(employee_id='101')  # or filter as needed
    html_string = render_to_string("csv_manager/attendance_pdf.html", {'attendance': attendance})
    html = HTML(string=html_string, base_url=request.build_absolute_uri())

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="attendance_report.pdf"'
    html.write_pdf(response)
    return response


# @login_required
# def export_employees_csv(request):
#     # Create the HTTP response with CSV content type
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="employees.csv"'

#     # Create a CSV writer
#     writer = csv.writer(response)
    
#     # Define the header row
#     writer.writerow([
#         "Employee Code", "Full Name", "Email", "Contact Number", 
#         "Date of Birth", "Gender", "Address", "Date of Joining", 
#         "Date of Leaving", "Position", "Department", "Leave Balance", 
#         "UID", "Created At", "Updated At"
#     ])
    
#     # Fetch all employees
#     employees = Employee.objects.all()

#     for emp in employees:
#         writer.writerow([
#             emp.employee_code if emp.employee_code else "",
#             emp.full_name,
#             emp.email if emp.email else "",
#             emp.contact_number if emp.contact_number else "",
#             emp.date_of_birth if emp.date_of_birth else "",
#             emp.gender if emp.gender else "",
#             emp.address if emp.address else "",
#             emp.date_of_joining if emp.date_of_joining else "",
#             emp.date_of_leaving if emp.date_of_leaving else "",
#             emp.position if emp.position else "",
#             emp.department.name if emp.department else "",
#             emp.leave_balance if emp.leave_balance else "{}",
#             emp.uid,
#             emp.created_at,
#             emp.updated_at
#         ])

#     return response