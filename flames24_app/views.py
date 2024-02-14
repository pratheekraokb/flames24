# example/views.py
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render



from django.shortcuts import render
from django.http import JsonResponse
from .models import Department
from django.views.decorators.csrf import csrf_exempt
from .forms import DepartmentForm
import json


def home(request):
    return render(request,"user_page/home.html")

def about(request):
    return render(request,"user_page/about.html")


def adminHome(request):
    return render(request,"admin_page/AdminHome.html")


def create_edit_department(request):
    return render(request, 'admin_page/CreateDepartment.html')

@csrf_exempt
def create_department(request):
    if request.method == 'POST':
        try:
            dept_name = request.POST.get('dept_name', '')
            if dept_name:
                department = Department(dept_name=dept_name)
                try:
                    department.save()
                except:
                    return HttpResponse(json.dumps({'message': 'Department didnt added. Try again !'}), content_type='application/json')
                return HttpResponse(json.dumps({'message': 'Department added successfully'}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'message': 'Department name is required'}), status=400, content_type='application/json')
        except:
            return HttpResponse(json.dumps({'message': 'Department didnt added. Try again !'}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'message': 'Invalid request method'}), status=405, content_type='application/json')