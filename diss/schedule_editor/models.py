from django.db import models


class Disciplines(models.Model):
    idDiscipline = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)


class Groups(models.Model):
    idGroup = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=30)


class GroupDiscipline(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    discipline = models.ForeignKey(Disciplines, on_delete=models.CASCADE, default=0)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, default=0)


class Students(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, default=0)


class StudentDiscipline(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    discipline = models.ForeignKey(Disciplines, on_delete=models.CASCADE, default=0)
    student = models.ForeignKey(Students, on_delete=models.CASCADE, default=0)


class Classrooms(models.Model):
    idGroup = models.IntegerField(primary_key=True, unique=True)
    number = models.CharField(max_length=50)
    build = models.CharField(max_length=50)


class Teachers(models.Model):
    idGroup = models.IntegerField(primary_key=True, unique=True)
    fullname = models.CharField(max_length=50)


class Events(models.Model):
    idEvent = models.IntegerField(primary_key=True, unique=True)
    idDiscipline = models.ForeignKey(Disciplines, on_delete=models.CASCADE, default=0)
    idClassroom = models.ForeignKey(Classrooms, on_delete=models.CASCADE, default=0)
    idTeacher = models.ForeignKey(Teachers, on_delete=models.CASCADE, default=0)
    begin = models.DateTimeField('begin')
    end = models.DateTimeField('end')
    type = models.CharField(max_length=30)
    description = models.TextField()
