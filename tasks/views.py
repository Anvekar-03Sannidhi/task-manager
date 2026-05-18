import math

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q

from .models import Task


# HOME
def home(request):
    return render(request, 'home.html')


# SIGNUP
def signup(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('/login/')

    return render(request, 'signup.html')


# LOGIN
def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            next_url = request.GET.get('next')

            if next_url:
                return redirect(next_url)

            return redirect('/tasks/')

        else:
            return render(
                request,
                'login.html',
                {'error': 'Invalid Credentials'}
            )

    return render(request, 'login.html')


# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('/login/')


# TASK LIST
@login_required
def task_list(request):

    # FILTERS
    filter_type = request.GET.get('filter', 'ALL').upper()
    task_type = request.GET.get('type')

    today = timezone.now().date()

    #tasks still pending today
    today_tasks = Task.objects.filter(
        user = request.user,
        next_due=today
    )

    #tasks completed today
    completed_today_tasks = Task.objects.filter(
        user=request.user,
        last_completed = today
    )

    # USER TASKS
    tasks = Task.objects.filter(user=request.user)

    # MY DAY
    if not task_type:
        tasks = today_tasks        
    # SIDEBAR TYPE FILTERS
    else:
        tasks = tasks.filter(task_type=task_type)

    # STATUS FILTERS
    if filter_type == "PENDING":
        tasks = tasks.filter(status="PENDING")

    elif filter_type == "COMPLETED":
        tasks = tasks.filter(status="COMPLETED")

    # SEARCH
    search = request.GET.get('search')

    if search:
        tasks = tasks.filter(title__icontains=search)

    # STATS
    total_tasks = (
        today_tasks.count() + completed_today_tasks.count()
    )

    completed_tasks = completed_today_tasks.count()

    pending_tasks = today_tasks.count()

    # PROGRESS
    radius = 70
    circumference = 2 * math.pi * radius

    if total_tasks > 0:
        progress = int(
            (completed_tasks / total_tasks) * 100
        )
    else:
        progress = 0

    arc = circumference - (
        circumference * progress / 100
    )

    # CONTEXT
    context = {
        'tasks': tasks,
        'filter': filter_type,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'progress': progress,
        'arc': arc,
    }

    return render(
        request,
        'task_list.html',
        context
    )

# CREATE TASK
@login_required
def create_task(request):

    if request.method == 'POST':

        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')

        task_type = request.POST.get('task_type')
        custom_date = request.POST.get('custom_date') or None

        today = timezone.now().date()

        #Set next due
        if task_type == "CUSTOM":
            next_due = custom_date
        else:
            next_due = today

        Task.objects.create(
            user=request.user,
            title=title,
            description=description,
            priority=priority,
            task_type=task_type,
            custom_date=custom_date,
            next_due=next_due,
            status="PENDING"
        )

        return redirect('/tasks/')

    return render(request, 'create_task.html')


# EDIT TASK
@login_required
def edit_task(request, id):

    task = Task.objects.get(
        id=id,
        user=request.user
    )

    if request.method == 'POST':

        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.priority = request.POST.get('priority')
        task.status = request.POST.get('status')

        task.save()

        return redirect('/tasks/')

    return render(
        request,
        'edit_task.html',
        {'task': task}
    )


# DELETE TASK
@login_required
def delete_task(request, id):

    task = Task.objects.get(
        id=id,
        user=request.user
    )

    task.delete()

    return redirect('/tasks/')


# COMPLETE TASK
@login_required
def complete_task(request, id):

    task = Task.objects.get(
        id=id,
        user=request.user
    )

    today = timezone.now().date()

    #save completion date
    task.last_completed = today

    #Daily
    if task.task_type == "DAILY":
        task.next_due = today + timezone.timedelta(days=1)

    #weekly
    elif task.task_type == "WEEKLY":
        task.next_due = today + timezone.timedelta(days=7)
    #monthly
    elif task.task_type == "MONTHLY":
        if today.month == 12:
            task.next_due = today.replace(
                year=today.year + 1,
                month = 1
            )
        else:
            task.next_due = today.replace(
                month = today.month + 1
            )
    #yearly
    elif task.task_type == "YEARLY":

        task.next_due = today.replace(
            year = today.year + 1
        )

    #custom
    elif task.task_type == "CUSTOM":

        current_due = task.next_due

        task.next_due = current_due.replace(
            year = current_due.year + 1
        )
    
    #Reset status
    task.status = "PENDING"

    task.save()

    return redirect('/tasks/')

# SKIP TASK
@login_required
def skip_task(request, id):

    task = Task.objects.get(
        id=id,
        user=request.user
    )

    today = timezone.now().date()

    #Daily
    if task.task_type == "DAILY":
        task.next_due = today + timezone.timedelta(days=1)

    #weekly
    elif task.task_type == "WEEKLY":
        task.next_due = today + timezone.timedelta(days=7)
    #monthly
    elif task.task_type == "MONTHLY":
        if today.month == 12:
            task.next_due = today.replace(
                year = today.year + 1,
                month=1
            )
        else:
            task.next_due = today.replace(
                month = today.month + 1
            )
    #yearly
    elif task.task_type == "YEARLY":
        task.next_due = today.replace(
            year = today.year + 1
        )
    #custom
    elif task.task_type == "CUSTOM":
        current_due = task.next_due
        task.next_due = current_due.replace(
            year = current_due.year + 1
        )

    task.last_completed = None
    task.save()

    return redirect('/tasks/')