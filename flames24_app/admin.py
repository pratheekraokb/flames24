from django.contrib import admin

# Register your models here.
from .models import Event, Department, Winner, DepartmentResult

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_name', 'event_type', 'event_date')
    list_filter = ('event_type', 'event_date')
    search_fields = ('event_name',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'dept_name')
    search_fields = ('dept_name',)

@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'position', 'department', 'class_name')
    list_filter = ('position', 'department')
    search_fields = ('class_name',)

@admin.register(DepartmentResult)
class DepartmentResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'department', 'total_points')
    search_fields = ('department__dept_name',)