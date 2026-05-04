from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Task
from django.shortcuts import render, redirect
from django.utils import timezone

# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        User.objects.create_user(username=username, password=password) #create new user in DB
        return redirect('/login/')
    
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print("Username:", username)

        user = authenticate(request, username=username, password=password) #check if user exists and password is correct

        print("User:", user)

        if user is not None:
            login(request, user)
            
            next_url = request.GET.get('next')
            print("Next URL:", next_url)

            if next_url:
                return redirect(next_url)
            else:
                return redirect('/tasks/')
        else:
            print("Authentication failed")
            return render(request, 'login.html', {'error':'Invalid Credentials'})
        
    return render(request, 'login.html')
    
def logout_view(request):
    logout(request) 
    return redirect('/login/')

@login_required
def task_list(request):

    # GET FILTER
    filter_type = request.GET.get('filter', 'ALL').upper()

    # BASE QUERY
    tasks = Task.objects.filter(user=request.user)

    # APPLY FILTER
    if filter_type == "PENDING":
        tasks = tasks.filter(status="PENDING")

    elif filter_type == "COMPLETED":
        tasks = tasks.filter(status="COMPLETED")

    # SEARCH (keep if you already had it)
    search = request.GET.get('search')
    if search:
        tasks = tasks.filter(title__icontains=search)

    # STATS
    total_tasks = Task.objects.filter(user=request.user).count()
    completed_tasks = Task.objects.filter(user=request.user, status='COMPLETED').count()
    pending_tasks = Task.objects.filter(user=request.user, status='PENDING').count()

    # Calculate progress %
    if total_tasks > 0:
        progress = int((completed_tasks / total_tasks) * 100)
    else:
        progress = 0

    # 👇 THIS IS WHERE YOU ADD FILTER IN CONTEXT
    context = {
        'tasks': tasks,
        'filter': filter_type,   # ⭐ THIS LINE
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'progress': progress,
    }

    return render(request, 'task_list.html', context)  

@login_required
def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        deadline = request.POST.get('deadline')

        Task.objects.create(
            user=request.user,
            title=title,
            description=description,
            priority=priority,
            deadline=deadline
        )

        return redirect('/tasks/')

    return render(request, 'create_task.html')

@login_required
def edit_task(request, id):
    task = Task.objects.get(id=id, user=request.user)

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.priority = request.POST.get('priority')
        task.status = request.POST.get('status')
        task.deadline = request.POST.get('deadline')

        task.save()
        return redirect('/tasks/')
    
    return render(request, 'edit_task.html', {'task':task})

@login_required
def delete_task(request, id):
    task = Task.objects.get(id=id, user=request.user)
    task.delete()
    return redirect('/tasks/')

def complete_task(request, id):
    task = Task.objects.get(id=id)
    task.status = "COMPLETED"
    task.save()
    return redirect('/tasks/')

def skip_task(request, id):
    task = Task.objects.get(id=id)
    task.status = "SKIPPED"
    task.save()
    return redirect('/tasks/')