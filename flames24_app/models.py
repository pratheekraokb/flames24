from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=100)
    event_type = models.CharField(choices=(('Men', 'Men'), ('Women', 'Women')), max_length=5)
    event_date = models.DateField()

class Department(models.Model):
    id = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.dept_name


class Winner(models.Model):
    id = models.AutoField(primary_key=True)
    POSITION_CHOICES = (
        ('First', 'First'),
        ('Second', 'Second'),
        ('Third', 'Third'),
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    position = models.CharField(choices=POSITION_CHOICES, max_length=10)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=100)  # Assuming class is a string value like "S1…

class DepartmentResult(models.Model):
    id = models.AutoField(primary_key=True)
    department = models.OneToOneField(Department, on_delete=models.CASCADE)
    total_points = models.IntegerField(default=0)

@receiver(post_save, sender=Winner)
def update_department_points(sender, instance, created, **kwargs):
    if created:
        department_result, created = DepartmentResult.objects.get_or_create(department=instance.department)
        department_result.total_points += instance.points
        department_result.save()
