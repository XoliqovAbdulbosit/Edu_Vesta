from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Subject(models.Model):
    subject = models.CharField(max_length=45)

    def __str__(self):
        return self.subject


class Grade(models.Model):
    grade = models.IntegerField()

    def __str__(self):
        return str(self.grade)


class Lesson(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    link = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    answer = models.CharField(max_length=45)
    wrong_answer_1 = models.CharField(max_length=45)
    wrong_answer_2 = models.CharField(max_length=45)
    wrong_answer_3 = models.CharField(max_length=45)
    wrong_answer_4 = models.CharField(max_length=45)
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    percentage = models.IntegerField()

    class Meta:
        ordering = ['percentage']

    def __str__(self):
        return self.title


class Solved(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    task = models.ForeignKey(Task, on_delete=models.PROTECT)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('user', 'task')

    def __str__(self):
        return str(self.user) + ' ' + str(self.task)


class Sent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    cnt = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user) + ' ' + str(self.subject)


class Error(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    cnt = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user) + ' ' + str(self.subject)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    cnt = models.IntegerField(default=0)

    class Meta:
        ordering = ['-cnt']

    def __str__(self):
        return str(self.user)


class Olympiad(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    tasks = models.ManyToManyField(Task)

    def __str__(self):
        return str(self.name)


class Participants(models.Model):
    olympiad = models.ForeignKey(Olympiad, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    cnt = models.IntegerField(default=0)

    class Meta:
        ordering = ['-cnt']

    def __str__(self):
        return str(self.olympiad) + ' ' + str(self.user)
