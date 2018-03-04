from django.db import models


class Discipline(models.Model):
    name = models.CharField('наименование', max_length=100)

    class Meta:
        verbose_name = 'дисциплина'
        verbose_name_plural = 'дисциплины'
        ordering = ['name']

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField('наименование', max_length=30)
    disciplines = models.ManyToManyField('Discipline', verbose_name='дисциплины')

    class Meta:
        verbose_name = 'группа'
        verbose_name_plural = 'группы'


class Student(models.Model):
    fullname = models.CharField('полное имя', max_length=50)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    disciplines = models.ManyToManyField('Discipline', verbose_name='дисциплины')

    class Meta:
        verbose_name = 'студент'
        verbose_name_plural = 'студенты'


class Room(models.Model):
    """ Аудитории """
    number = models.CharField('номер', max_length=50)
    building = models.CharField('здание', max_length=50)

    class Meta:
        verbose_name = 'аудитория'
        verbose_name_plural = 'аудитории'
        ordering = ['building', 'number']

    def __str__(self):
        return self.building + ' ' + self.number


class Teacher(models.Model):
    """ Преподаватели """
    last_name = models.CharField('фамилия', max_length=50)
    first_name = models.CharField('имя', max_length=50)
    second_name = models.CharField('отчество', max_length=50, blank=True, default='')
    user = models.OneToOneField('auth.User', on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        verbose_name = 'преподаватель'
        verbose_name_plural = 'преподаватели'
        ordering = ['last_name', 'first_name', 'second_name']

    def __str__(self):
        return '%s %s %s' % (self.last_name, self.first_name, self.second_name)


class Event(models.Model):
    """ События """
    discipline = models.ForeignKey('Discipline', on_delete=models.CASCADE, blank=True, null=True,
                                   verbose_name='дисциплина')
    room = models.ForeignKey('Room', on_delete=models.CASCADE, verbose_name='аудитория')
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, blank=True, null=True,
                                verbose_name='преподаватель')
    begin = models.DateTimeField('начало')
    end = models.DateTimeField('окончание')
    event_type = models.CharField('тип события', max_length=30)
    description = models.TextField('описание')

    class Meta:
        verbose_name = 'событие'
        verbose_name_plural = 'события'
