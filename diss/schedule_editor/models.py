from django.db import models


class Discipline(models.Model):
    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'
        ordering = ['name']

    name = models.CharField('Наименование', max_length=100)

    def __str__(self):
        return self.name


class Group(models.Model):
    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    name = models.CharField('Наименование', max_length=30)
    disciplines = models.ManyToManyField('Discipline', verbose_name='Дисциплины')


class Student(models.Model):
    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    fullname = models.CharField('Полное имя', max_length=50)
    group = models.ForeignKey('Group')
    disciplines = models.ManyToManyField('Discipline', verbose_name='Дисциплины')


class Classroom(models.Model):
    class Meta:
        verbose_name = 'Аудитория'
        verbose_name_plural = 'Аудитории'
        ordering = ['number']

    number = models.CharField('Номер', max_length=50)
    build = models.CharField('Здание', max_length=50)

    def __str__(self):
        return self.number + ' ' + self.build

class Teacher(models.Model):
    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
        # ordering = ['name']

    fullname = models.CharField('Полное имя', max_length=50)

    def __str__(self):
        return self.fullname


class Event(models.Model):
    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    discipline = models.ForeignKey('Discipline', verbose_name='Дисциплина', blank=True, null=True)
    classroom = models.ForeignKey('Classroom', verbose_name='Аудитория')
    teacher = models.ForeignKey('Teacher', verbose_name='Преподаватель', blank=True, null=True)
    begin = models.DateTimeField('Начало')
    end = models.DateTimeField('Окончание')
    event_type = models.CharField('Тип события', max_length=30)
    description = models.TextField('Описание')

