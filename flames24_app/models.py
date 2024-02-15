from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=100)
    event_type = models.CharField(choices=(('Men', 'Men'), ('Women', 'Women')), max_length=5)
    event_date = models.DateField()

    class Meta:
        unique_together = ['event_name', 'event_type']
        db_table = 'Events'

    def __str__(self):
        return f"{self.event_name} ({self.event_type})"

class Department(models.Model):
    id = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'Department'

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
    winner_athlete = models.CharField(max_length=200, blank=True, default="")
    position = models.CharField(choices=POSITION_CHOICES, max_length=10)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=100)  # Assuming class is a string value like "S1…
    points = models.IntegerField(default=0)

    class Meta:
        db_table = 'Winner'
        unique_together = ['event', 'winner_athlete', 'position']

class DepartmentResult(models.Model):
    id = models.AutoField(primary_key=True)
    department = models.OneToOneField(Department, on_delete=models.CASCADE)
    total_points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.department}: {self.total_points} points"
    
    class Meta:
        db_table = 'DepartmentResult'

    

@receiver(post_save, sender=Winner)
def update_department_points(sender, instance, created, **kwargs):
    if created:
        department_result, created = DepartmentResult.objects.get_or_create(department=instance.department)
        department_result.total_points += instance.points
        department_result.save()


class Image(models.Model):
    image_id = models.CharField(max_length=100, unique=True)
    image_url = models.URLField()

    def __str__(self):
        return self.image_id