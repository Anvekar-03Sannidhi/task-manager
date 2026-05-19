from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('tasks/',views.task_list),
    path('create-task/', views.create_task),
    path('edit-task/<int:id>/', views.edit_task),
    path('delete-task/<int:id>/', views.delete_task),
    path('complete-task/<int:id>/', views.complete_task),
    path('skip-task/<int:id>/', views.skip_task),
    path('undo-task/<int:id>/', views.undo_task, name='undo_task'),
]
