from django.db import models #models = blueprint for DB
from django.contrib.auth.models import User #importing User model to link tasks to specific users (if needed)

# Create your models(table) here.

class Task(models.Model): #Database table for tasks-> connected to admin panel-> created DB structure using migrations
    STATUS_CHOICE = [
        ('PENDING', 'Pending'), # First value → stored in DB (PENDING), Second value → shown to user (Pending)
        ('COMPLETED', 'Completed'),
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]

    TASK_TYPES = [
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('YEARLY', 'Yearly'),
        ('CUSTOM', 'Custom'),
    ]

    task_type = models.CharField(
        max_length=20,
        choices=TASK_TYPES,
        default='DAILY'
    )

    custom_date = models.DateField(null=True, blank=True)
    next_due = models.DateField(null=True, blank=True) 

    title = models.CharField(max_length=200) 
    description = models.TextField() 
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='PENDING') 
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    deadline = models.DateField(null=True, blank=True) 
    created_at = models.DateField(auto_now_add=True) 
    last_completed = models.DateField(null=True, blank=True) 
    previous_due = models.DateField(null=True, blank=True)

    def __str__(self): #This controls how object appears in admin panel
        return self.title
    
    #ForeignKey creates a relationship between Task and User models,
    user = models.ForeignKey(User, on_delete=models.CASCADE) #user dlt -> all their tasks dlt (CASCADE)
    