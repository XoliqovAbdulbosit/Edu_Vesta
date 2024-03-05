from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout, name='logout'),
    path('lessons/<int:subject_id>/', lessons_by_subject, name='lessons'),
    path('lessons/<int:subject_id>/<int:grade_id>/', lessons_by_grade, name='lessons'),
    path('lesson/<int:lesson_id>/', lesson, name='lesson'),
    path('tasks/', tasks, name='tasks'),
    path('tasks/<int:subject_id>', tasks_by_subject, name='tasks'),
    path('task/<int:task_id>', task, name='task'),
    path('profile/<int:user_id>', profile, name='profile'),
    path('rating/', rating, name='rating'),
    path('olympiads/', olympiads, name='olympiads'),
    path('olympiad/<int:olympiad_id>', olympiad, name='olympiad'),
    path('olympiad_tasks/<int:olympiad_id>', olympiad_tasks, name='olympiad_tasks'),
]
