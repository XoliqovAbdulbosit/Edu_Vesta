from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login as user_login, logout as user_logout, authenticate
from .models import *


# Create your views here.
def home(request):
    subjects = Subject.objects.all()
    return render(request, 'home.html', {'subjects': subjects})


def tasks(request):
    subjects = Subject.objects.all()
    tasks = Task.objects.all()
    return render(request, 'tasks.html', {'subjects': subjects, 'tasks': tasks})


def tasks_by_subject(request, subject_id):
    subjects = Subject.objects.all()
    tasks = Task.objects.filter(subject=subject_id)
    return render(request, 'tasks.html', {'subjects': subjects, 'tasks': tasks})


def task(request, task_id):
    subjects = Subject.objects.all()
    task = Task.objects.get(pk=task_id)
    if request.method == 'POST':
        sent = Sent.objects.get_or_create(user=request.user, subject=task.subject)
        sent[0].cnt += 1
        sent[0].save()
        if request.POST.get('flexRadioDefault') == task.answer:
            solved = Solved.objects.get_or_create(user=request.user, task=task, subject=task.subject)
            profile = Profile.objects.get(user=request.user)
            if solved[1]:
                profile.cnt += 1
                profile.save()
                solved[0].save()
            messages.success(request, 'You are right :)')
        else:
            error = Error.objects.get_or_create(user=request.user, subject=task.subject)
            error[0].cnt += 1
            error[0].save()
            messages.error(request, 'Wrong answer :(')
    return render(request, 'task.html', {'subjects': subjects, 'task': task})


def rating(request):
    subjects = Subject.objects.all()
    profiles = Profile.objects.all()
    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user=request.user)
        rank = list(Profile.objects.all().values_list('user', flat=True)).index(request.user.pk) + 1
    else:
        user_profile = ''
        rank = ''
    return render(request, 'rating.html', {'subjects': subjects, 'profiles': profiles, 'user_profile': user_profile, 'rank': rank})


def profile(request, user_id):
    subjects = Subject.objects.all()
    ln = Task.objects.all().count()
    user = User.objects.get(pk=user_id)
    profile = Profile.objects.get(user=user_id)
    rank = list(Profile.objects.all().values_list('user', flat=True)).index(user_id) + 1
    dct = list()
    for subject in subjects:
        solved = Solved.objects.filter(user=user_id, subject=subject).count()
        try:
            sent = Sent.objects.get(user=user_id, subject=subject).cnt
        except:
            sent = 0
        try:
            error = Error.objects.get(user=user_id, subject=subject).cnt
        except:
            error = 0
        dct.append([subject, solved, sent, error])
    return render(request, 'profile.html', {'subjects': subjects, 'ln': ln, 'profile': profile, 'users': user, 'dct': dct, 'rank': rank})


def lessons_by_subject(request, subject_id):
    lessons = Lesson.objects.filter(subject=subject_id)
    subjects = Subject.objects.all()
    current = Subject.objects.get(pk=subject_id)
    grades = Grade.objects.all()
    return render(request, 'lessons.html', {'lessons': lessons, 'name': current, 'subjects': subjects, 'grades': grades})


def lessons_by_grade(request, subject_id, grade_id):
    lessons = Lesson.objects.filter(subject=subject_id, grade=grade_id)
    subjects = Subject.objects.all()
    current = Subject.objects.get(pk=subject_id)
    grades = Grade.objects.all()
    return render(request, 'lessons.html', {'lessons': lessons, 'name': current, 'subjects': subjects, 'grades': grades})


def lesson(request, lesson_id):
    subjects = Subject.objects.all()
    lesson = Lesson.objects.get(pk=lesson_id)
    return render(request, 'lesson.html', {'subjects': subjects, 'lesson': lesson})


def olympiads(request):
    olympiads = Olympiad.objects.all()
    subjects = Subject.objects.all()
    return render(request, 'olympiads.html', {'olympiads': olympiads, 'subjects': subjects})


def olympiad(request, olympiad_id):
    olympiad = Olympiad.objects.get(pk=olympiad_id)
    subjects = Subject.objects.all()
    return render(request, 'olympiad.html', {'olympiad': olympiad, 'subjects': subjects})


def olympiad_tasks(request, olympiad_id):
    olympiad = Olympiad.objects.get(pk=olympiad_id)
    if request.method == 'POST':
        participant = Participants.objects.create(olympiad=Olympiad.objects.get(pk=olympiad_id), user=request.user)
        lst = []
        for i in range(1, len(olympiad.tasks.all()) + 1):
            lst.append(request.POST.get(f'answer_{i}'))
        ans = []
        for task in olympiad.tasks.all():
            ans.append(task.answer)
        score = 0
        for i in range(len(ans)):
            if lst[i] == ans[i]:
                score += 1
        participant.cnt = score
        participant.save()
        return redirect('olympiads')
    else:
        subjects = Subject.objects.all()
        return render(request, 'olympiad_tasks.html', {'olympiad': olympiad, 'subjects': subjects})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            user_login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            profile.save()
            return redirect('login')
    return render(request, 'signup.html')


def logout(request):
    if request.method == 'POST':
        user_logout(request)
        return redirect('home')
