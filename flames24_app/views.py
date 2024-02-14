# example/views.py
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render



from django.shortcuts import render
from django.http import JsonResponse
from .models import Department, Event, Winner
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


def fetch_departments(request):
    departments = Department.objects.all()
    data = [{'id': department.id, 'name': department.dept_name} for department in departments]
    return JsonResponse({'success': True, 'departments': data})

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
            if not event_name:
                return JsonResponse({'message': 'Event name is required.'}, status=400)
            if event_type not in ['Men', 'Women']:
                return JsonResponse({'message': 'Invalid event type.'}, status=400)
            event = Event.objects.create(event_name=event_name, event_type=event_type, event_date=event_date)

            return JsonResponse({'message': 'Event created successfully!', 'id': event.id}, status=201)

        except Exception as e:
            return JsonResponse({'message': 'An error occurred: ' + str(e)})
   
def add_winners(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        winner_count = request.POST.get('winner_count', 1)
        winner_count = int(winner_count)
        print(winner_count)

        # Validate event ID and fetch event details
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return JsonResponse({'message': 'Invalid event ID.'}, status=400)

        winners = []
        for i in range(1, winner_count + 1):
            player = request.POST.get(f'winner_athlete_{i}')
            position = request.POST.get(f'position_{i}')
            department_id = request.POST.get(f'department_{i}')
            class_name = request.POST.get(f'class_name_{i}')
            points = request.POST.get(f'points_{i}')

            points = int(points)

            # Validate winner data
            if not player or not position or not department_id or not class_name or not points:
                return JsonResponse({'message': 'Missing required winner data.'}, status=400)

            try:
                department = Department.objects.get(pk=department_id)
            except Department.DoesNotExist:
                return JsonResponse({'message': 'Invalid department ID.'}, status=400)

            try:
                winner = Winner.objects.create(
                    winner_athlete=player,
                    event=event,
                    position=position,
                    department=department,
                    class_name=class_name,
                    points=points
                )
                winners.append(winner)
            except Exception as e:
                return JsonResponse({'message': str(e)}, status=400)

        # Handle winner creation success
        print("Winners added successfully:", winners)
        return JsonResponse({'message': 'Winners added successfully.'}, status=201)
    elif request.method == 'GET':
        # GET request (initial form):
        events = Event.objects.all()
        departments = Department.objects.all()

        context = {
            'events': events,
            'departments': departments,
        }

        return render(request, 'admin_page/AddingWinners.html', context)