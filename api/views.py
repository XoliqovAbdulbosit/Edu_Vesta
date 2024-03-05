import json
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from main.models import *


# Create your views here.
def categories(request):
    subjects = Subject.objects.values_list('subject', flat=True)
    return JsonResponse(list(subjects), safe=False)


def grades(request):
    grades = Grade.objects.values_list('grade', flat=True)
    return JsonResponse(list(grades), safe=False)


def lessons(request):
    lessons = Lesson.objects.all().values_list('title', flat=True)
    return JsonResponse(list(lessons), safe=False)


def lessons_by_subject(request, subject):
    lessons = Lesson.objects.filter(subject=Subject.objects.get(subject=subject)).values_list('title', flat=True)
    return JsonResponse(list(lessons), safe=False)


def lessons_by_grade(request, grade):
    lessons = Lesson.objects.filter(grade=Grade.objects.get(grade=grade)).values_list('title', flat=True)
    return JsonResponse(list(lessons), safe=False)


def lessons_by_subject_grade(request, subject, grade):
    lessons = Lesson.objects.filter(subject=Subject.objects.get(subject=subject), grade=Grade.objects.get(grade=grade)).values_list('title', flat=True)
    return JsonResponse(list(lessons), safe=False)


def tasks(request):
    tasks = Task.objects.all().values_list('title', flat=True)
    return JsonResponse(list(tasks), safe=False)


def tasks_by_subject(request, subject):
    tasks = Task.objects.filter(subject=Subject.objects.get(subject=subject)).values_list('title', flat=True)
    return JsonResponse(list(tasks), safe=False)


def tasks_by_grade(request, grade):
    tasks = Task.objects.filter(grade=Grade.objects.get(grade=grade)).values_list('title', flat=True)
    return JsonResponse(list(tasks), safe=False)


def tasks_by_subject_grade(request, subject, grade):
    tasks = Task.objects.filter(subject=Subject.objects.get(subject=subject), grade=Grade.objects.get(grade=grade)).values_list('title', flat=True)
    return JsonResponse(list(tasks), safe=False)


def lesson(request, lesson):
    fnd = Lesson.objects.get(title=lesson)
    data = {
        'title': fnd.title,
        'content': fnd.content,
        'grade': fnd.grade.grade,
        'subject': fnd.subject.subject,
        'link': fnd.link
    }
    return JsonResponse(data, safe=False)


def task(request, task):
    fnd = Task.objects.get(title=task)
    data = {
        'title': fnd.title,
        'content': fnd.content,
        'answer': fnd.answer,
        'wrong_answer_1': fnd.wrong_answer_1,
        'wrong_answer_2': fnd.wrong_answer_2,
        'wrong_answer_3': fnd.wrong_answer_3,
        'wrong_answer_4': fnd.wrong_answer_4,
        'grade': fnd.grade.grade,
        'subject': fnd.subject.subject,
        'percentage': fnd.percentage
    }
    return JsonResponse(data, safe=False)


@csrf_exempt
def task_submit(request, user, task):
    fnd = Task.objects.get(title=task)
    sent = Sent.objects.get_or_create(user=User.objects.get(username=user), subject=fnd.subject)
    sent[0].cnt += 1
    sent[0].save()
    if request.body.decode('utf-8').strip('"') == fnd.answer:
        solved = Solved.objects.get_or_create(user=User.objects.get(username=user), task=fnd, subject=fnd.subject)
        profile = Profile.objects.get(user=User.objects.get(username=user))
        if solved[1]:
            profile.cnt += 1
            profile.save()
            solved[0].save()
        return JsonResponse("To'g'ri javob", safe=False)
    else:
        error = Error.objects.get_or_create(user=User.objects.get(username=user), subject=fnd.subject)
        error[0].cnt += 1
        error[0].save()
        return JsonResponse("Noto'g'ri javob", safe=False)


def olympiads(request):
    olympiads = Olympiad.objects.values_list('name', flat=True)
    return JsonResponse(list(olympiads), safe=False)


def olympiad(request, olympiad):
    fnd = Olympiad.objects.get(name=olympiad)
    data = {
        'name': fnd.name,
        'start_time': fnd.start_time,
        'end_time': fnd.end_time,
        'tasks': list(fnd.tasks.values('title', 'content', 'answer', 'wrong_answer_1', 'wrong_answer_2', 'wrong_answer_3', 'wrong_answer_4', 'grade', 'subject', 'percentage')),
    }
    return JsonResponse(data, safe=False)


@csrf_exempt
def olympiad_submit(request, user, olympiad):
    participant = Participants.objects.create(olympiad=Olympiad.objects.get(name=olympiad), user=User.objects.get(username=user))
    fnd = Olympiad.objects.get(name=olympiad)
    lst = json.loads(request.body.decode('utf-8'))
    ans = []
    for task in fnd.tasks.all():
        ans.append(task.answer)
    score = 0
    for i in range(len(ans)):
        if lst[i] == ans[i]:
            score += 1
    participant.cnt = score
    participant.save()
    return JsonResponse(score, safe=False)


def register(request, username, password):
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username=username, password=password)
        user.save()
        profile = Profile.objects.create(user=user)
        profile.save()
        return JsonResponse("Success", safe=False)
    else:
        return JsonResponse("Username already exists", safe=False)


def rating(request):
    rating = Profile.objects.values('user__username', 'cnt')
    return JsonResponse(list(rating), safe=False)


def login(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        return JsonResponse("Success", safe=False)
    else:
        return JsonResponse("Fail", safe=False)
