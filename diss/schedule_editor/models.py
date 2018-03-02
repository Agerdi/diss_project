from django.db import models


class Discipline(models.Model):
    name = models.CharField('Наименование', max_length=100)

    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'
        ordering = ['name']

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField('Наименование', max_length=30)
    disciplines = models.ManyToManyField('Discipline', verbose_name='Дисциплины')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Student(models.Model):
    fullname = models.CharField('Полное имя', max_length=50)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    disciplines = models.ManyToManyField('Discipline', verbose_name='Дисциплины')

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'


class Classroom(models.Model):
    number = models.CharField('Номер', max_length=50)
    build = models.CharField('Здание', max_length=50)

    class Meta:
        verbose_name = 'Аудитория'
        verbose_name_plural = 'Аудитории'
        ordering = ['number']

    def __str__(self):
        return self.number + ' ' + self.build


class Teacher(models.Model):
    fullname = models.CharField('Полное имя', max_length=50)

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
        # ordering = ['name']

    def __str__(self):
        return self.fullname


class Event(models.Model):
    discipline = models.ForeignKey('Discipline', on_delete=models.CASCADE, blank=True, null=True,
                                   verbose_name='Дисциплина')
    classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE, verbose_name='Аудитория')
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, blank=True, null=True,
                                verbose_name='Преподаватель')
    begin = models.DateTimeField('Начало')
    end = models.DateTimeField('Окончание')
    event_type = models.CharField('Тип события', max_length=30)
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
