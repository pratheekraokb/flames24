# example/urls.py
from django.urls import path

from flames24_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),


    path('adminSection/', views.adminHome, name="adminHome"),
    path('adminSection/create-department/', views.create_edit_department, name='create_edit_department'),
    path('adminSection/add-event/', views.addingEventsPage,name="addingEventPage"),

    path('adminSection/add-winners/', views.add_winners, name='add_winners'),
    path('dept-results/', views.deptResults, name="deptResults"),

    path('api/create-department/', views.create_department, name='create_department'),
    path('api/create-event/', views.create_event, name='createEvent'),
    path('fetch-departments/', views.fetch_departments, name='fetch_departments'),
    

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)