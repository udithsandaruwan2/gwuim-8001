from django.shortcuts import render

@api_view(['GET'])
def getEmployeeDetail(request, pk):
    """View to retrieve details of a specific employee."""
    employee = Employee.objects.get(uid=pk)
    serializer = EmployeeSerializer(employee, many=False)
    return Response(serializer.data)