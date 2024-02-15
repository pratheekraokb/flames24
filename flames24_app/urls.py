# example/urls.py
from django.urls import path

from flames24_app import views
from django.conf import settings

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),


    path('adminSection/', views.adminHome, name="adminHome"),
    path('adminSection/create-department/', views.create_edit_department, name='create_edit_department'),
    path('adminSection/add-event/', views.addingEventsPage,name="addingEventPage"),

    path('adminSection/add-winners/', views.add_winners, name='add_winners'),
    path('dept-results/', views.deptResults, name="deptResults"),
    path('admin-signin/', views.signIn, name="signIn"),
    path('events_listing/', views.eventsListing, name="eventsListing"),
    path('event_results/', views.eventsResults, name="eventsResults"),
    path('gallery/',views.gallery, name="gallery"),


    path('api/create-department/', views.create_department, name='create_department'),
    path('api/create-event/', views.create_event, name='createEvent'),
    path('api/eventwinners/<int:eventid>/', views.event_winners_api, name='event_winners_api'),
    path('fetch-departments/', views.fetch_departments, name='fetch_departments'),

    
    

]
