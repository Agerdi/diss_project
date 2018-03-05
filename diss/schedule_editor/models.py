from django.db import models

AUTUMN = 'AUT'
SPRING = 'SPR'

SEMESTER = (
    (AUTUMN, 'осенний'),
    (SPRING, 'весенний')
)


class Subject(models.Model):
    name = models.CharField('наименование', max_length=100)
    student_group = models.ForeignKey('StudentGroup', on_delete=models.CASCADE, verbose_name='учебная группа')
    year = models.IntegerField('календарный год')
    semester = models.CharField('семестр', max_length=3, choices=SEMESTER)
    lecture_hours = models.IntegerField('часы лекций', blank=True, default=0)
    lab_work_hours = models.IntegerField('часы лабораторных работ', blank=True, default=0)
    practice_hours = models.IntegerField('часы практических работ', blank=True, default=0)
    student_work_hours = models.IntegerField('часы СРС', blank=True, default=0)
    control_hours = models.IntegerField('часы КСР', blank=True, default=0)
    total_hours = models.IntegerField('часов всего', blank=True, default=0)

    class Meta:
        verbose_name = 'дисциплина'
        verbose_name_plural = 'дисциплины'
        ordering = ['name']

    def __str__(self):
        return self.name


class StudentGroup(models.Model):
    name = models.CharField('наименование', max_length=30)
    year = models.IntegerField('год поступления')

    class Meta:
        verbose_name = 'группа'
        verbose_name_plural = 'группы'
        ordering = ['year', 'name']

    def __str__(self):
        return self.name


class Student(models.Model):
    fullname = models.CharField('полное имя', max_length=50)
    student_group = models.ForeignKey('StudentGroup', on_delete=models.CASCADE)
    disciplines = models.ManyToManyField('Subject', verbose_name='дисциплины')

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
        return '%s, ауд. %s' % (self.building, self.number)


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
    discipline = models.ForeignKey('Subject', on_delete=models.CASCADE, blank=True, null=True,
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


class Semester(models.Model):
    """ График учебного процесса """
    student_group = models.ForeignKey('StudentGroup', on_delete=models.DO_NOTHING, verbose_name='учебная группа')
    year = models.IntegerField('календарный год')
    semester = models.CharField('семестр', max_length=3, choices=SEMESTER)
    begin_study = models.DateField('начало теоретического обучения')
    end_study = models.DateField('конец теоретического обучения')
    begin_exams = models.DateField('начало экзаменационной сессии')
    end_exams = models.DateField('конец экзаменационной сессии')

    class Meta:
        verbose_name = 'семестр'
        verbose_name_plural = 'график учебного процесса'

    def __str__(self):
        if self.semester == AUTUMN:
            begin = self.year
            end = self.year + 1
        else:
            begin = self.year - 1
            end = self.year
        return '%s: %d-%d учебный год, %s семестр' % (self.student_group.name, begin, end, self.get_semester_display())
