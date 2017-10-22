from django.db import models


class TrainingSessions(models.Model):
    idTrainingSessions = models.IntegerField(primary_key=True, unique=True)
    idDiscipline = models.IntegerField()
    idGroup = models.IntegerField()
    idClassroom = models.IntegerField()
    idTeacher = models.IntegerField()
    datetime = models.DateTimeField('date published')


class Groups(models.Model):
    idGroup = models.IntegerField(primary_key=True, unique=True)
    idTrainingSessions = models.ForeignKey(TrainingSessions, on_delete=models.CASCADE, default=0)
    idDiscipline = models.CharField(max_length=200)
    name = models.CharField(max_length=200)