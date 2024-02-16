# example/views.py
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render


from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import JsonResponse
from .models import Department, Event, Winner, Image
from django.views.decorators.csrf import csrf_exempt
from .forms import DepartmentForm
import json

from .models import DepartmentResult
from django.core.serializers import serialize


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
    

# def deptResults(request):
#     department_results = DepartmentResult.objects.all().order_by('-total_points')
#     return render(request, 'user_page/results.html', {'department_results': department_results})
from django.db import models


def calculate_department_points():
    department_results = DepartmentResult.objects.all().order_by('-total_points')

    department_points = {}
    for department_result in department_results:
        department_name = department_result.department.dept_name
        boys_points = Winner.objects.filter(event__event_type='Men', department=department_result.department).aggregate(sum_points=models.Sum('points'))['sum_points'] or 0
        girls_points = Winner.objects.filter(event__event_type='Women', department=department_result.department).aggregate(sum_points=models.Sum('points'))['sum_points'] or 0
        total_points = boys_points + girls_points
        department_points[department_name] = {
            'boys_points': boys_points,
            'girls_points': girls_points,
            'total_points': total_points
        }

    return department_points

def deptResults(request):
    department_results = DepartmentResult.objects.all().order_by('-total_points')
    department_points = calculate_department_points()

    mens_points = {}
    womens_points = {}
    
    for department_result in department_results:
        department_name = department_result.department.dept_name
        if department_name in department_points:
            boys_points = department_points[department_name]['boys_points']
            girls_points = department_points[department_name]['girls_points']
            mens_points[department_name] = boys_points
            womens_points[department_name] = girls_points

    # Sort mens_points and womens_points dictionaries by values (points) in descending order
    mens_points = {k: v for k, v in sorted(mens_points.items(), key=lambda item: item[1], reverse=True)}
    womens_points = {k: v for k, v in sorted(womens_points.items(), key=lambda item: item[1], reverse=True)}

   
    return render(request, 'user_page/results.html', {'mens_points': mens_points, 'womens_points': womens_points})


def signIn(request):
    return render(request,'user_page/signin.html')

def eventsListing(request):
    try:
        events = Event.objects.all().order_by('event_date')
        

        mens_events = Event.objects.filter(event_type='Men').order_by('event_date')
        womens_events = Event.objects.filter(event_type='Women').order_by('event_date')

        print(mens_events,womens_events)
        return render(request, 'user_page/events_listing.html', {'mens_events': mens_events, 'womens_events': womens_events})
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})
    

from django.http import JsonResponse
from .models import Winner
from django.shortcuts import get_object_or_404
import json

def event_winners_api(request, eventid):
    event_winners = {
        'EventName': '',
        'First': '',
        'Second': '',
        'Third': ''
    }
    try:
        eventid = int(eventid)
        event = get_object_or_404(Event, id=eventid)
        event_winners['EventName'] = str(event)
        for position in ['First', 'Second', 'Third']:
            winner = Winner.objects.filter(event_id=eventid, position=position).first()
            if winner:
                event_winners[position] = {
                    'winner_athlete': winner.winner_athlete,
                    'department_name': winner.department.dept_name,
                    'class_name': winner.class_name
                }
        return JsonResponse(event_winners)
    except Exception as e:
        return JsonResponse({'error': str(e)})
    

import logging

logger = logging.getLogger(__name__)

def eventsResults(request):
    try:
        events = Event.objects.all().order_by('event_date')
        mens_events = Event.objects.filter(event_type='Men').order_by('event_date')
        womens_events = Event.objects.filter(event_type='Women').order_by('event_date')

        print(mens_events, womens_events)
        return render(request, 'user_page/event_result.html', {'mens_events': mens_events, 'womens_events': womens_events})
    except Exception as e:
        logger.error("An error occurred: %s", e)
        return render(request, 'user_page/error.html', {'error_message': "An error occurred. Please try again later."})
# /home/user/Desktop/Projects/django_host/flames24/flames24_app/templates/user_page/event_result.html
    

def gallery(request):
    images = Image.objects.all()
    image_data = [{'id': image.image_id, 'url': image.image_url} for image in images]
    context = {'image_data': image_data}
    return render(request, 'user_page/gallary.html', context)

from urllib.parse import unquote

def get_winners_by_department_and_gender(request, department_name, character):
    try:
        department_name = unquote(department_name)
        character = unquote(character)

        if character.upper() == 'M':
            gender = 'Men'
        elif character.upper() == 'F':
            gender = 'Women'
        else:
            return JsonResponse({'error': 'Invalid gender character'}, status=400)

        winners = Winner.objects.filter(department__dept_name=department_name, event__event_type=gender)
        data = [{'event_name': winner.event.event_name, 'winner_athlete': winner.winner_athlete, 'position': winner.position, 'points': winner.points} for winner in winners]

        return JsonResponse({'winners': data})
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Department or gender not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)