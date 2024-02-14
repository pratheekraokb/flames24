# example/views.py
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render



from django.shortcuts import render
from django.http import JsonResponse
from .models import Department, Event
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

def addingEventsPage(request):
    return render(request, 'admin_page/AddingEvents.html')

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
    
@csrf_exempt
def create_event(request):
    if request.method == 'POST':
        try:
            event_name = request.POST['event_name']
            event_type = request.POST['event_type']
            event_date = request.POST['event_date']

            # Validate data (optional, improve based on your requirements)
            if not event_name:
                return JsonResponse({'message': 'Event name is required.'}, status=400)
            if event_type not in ['Men', 'Women']:
                return JsonResponse({'message': 'Invalid event type.'}, status=400)
            # ... further validation

            # Create event
            event = Event.objects.create(event_name=event_name, event_type=event_type, event_date=event_date)

            return JsonResponse({'message': 'Event created successfully!', 'id': event.id}, status=201)

        except Exception as e:
            return JsonResponse({'message': 'An error occurred: ' + str(e)})