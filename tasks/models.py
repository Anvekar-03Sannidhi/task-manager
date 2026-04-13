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

    title = models.CharField(max_length=200) #short textfield , with max len of 200 chars
    description = models.TextField() #long textfield, no max len
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='PENDING') #stores only PENDING or COMPLETED, default is PENDING
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM') #stores only LOW, MEDIUM or HIGH, default is MEDIUM
    deadline = models.DateTimeField() #Ex: 2024-06-30 23:59:00
    created_at = models.DateTimeField(auto_now_add=True) #automatically set to current date and time when task is created, cannot be changed later(set only once at creation)

    def __str__(self): #This controls how object appears in admin panel
        return self.title
    
    #ForeignKey creates a relationship between Task and User models,
    user = models.ForeignKey(User, on_delete=models.CASCADE) # on_delete=models.CASCADE means if user is deleted, all their tasks will also be deleted (cascading delete)