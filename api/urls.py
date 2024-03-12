from django.urls import path
from .views import *

urlpatterns = [
    path('categories/', categories),
    path('grades/', grades),
    path('lessons/', lessons),
    path('lessons/<subject>/<grade>', lessons_by_subject_grade),
    path('lesson/<lesson>', lesson),
    path('tasks/', tasks),
    path('tasks/<subject>/<grade>', tasks_by_subject_grade),
    path('task/<task>', task),
    path('task/<user>/<task>', task_submit),
    path('olympiads/', olympiads),
    path('olympiad/<olympiad>', olympiad),
    path('olympiad/<user>/<olympiad>', olympiad_submit),
    path('rating/', rating),
    path('profile/<username>', profile),
    path('register/<username>/<password>', register),
    path('login/<username>/<password>', login)
]
