from datetime import datetime

from django.db.models import (CASCADE, CharField, DateField, DateTimeField, DO_NOTHING, ForeignKey, IntegerField, Model,
                              OneToOneField, TextField)


class Subject(Model):
    """ Дисциплина """

    name = CharField('наименование', max_length=100)
    semester = ForeignKey('Semester', on_delete=CASCADE, verbose_name='семестр')
    lecture_hours = IntegerField('часы лекций', blank=True, default=0)
    lab_work_hours = IntegerField('часы лабораторных работ', blank=True, default=0)
    practice_hours = IntegerField('часы практических работ', blank=True, default=0)
    student_work_hours = IntegerField('часы СРС', blank=True, default=0)
    control_hours = IntegerField('часы КСР', blank=True, default=0)
    total_hours = IntegerField('часов всего', blank=True, default=0)

    class Meta:
        verbose_name = 'дисциплина'
        verbose_name_plural = 'дисциплины'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_total_hours(self):
        return self.lecture_hours + self.lab_work_hours + self.practice_hours + self.student_work_hours + self.control_hours 


class SubjectClass(Model):
    """ Занятие дисциплины """

    LECTURE = 'LEC'
    LAB_WORK= 'LAB'
    PRACTICE = 'PRA'

    CLASS_TYPES = (
        (LECTURE, 'лекция'),
        (LAB_WORK, 'лабораторная работа'),
        (PRACTICE, 'практическое занятие')
    )

    MONDAY = 'MON'
    TUESDAY = 'TUE'
    WEDNESDAY = 'WED'
    THURSDAY = 'THU'
    FRIDAY = 'FRI'
    SATURDAY = 'SAT'
    SUNDAY = 'SUN'

    WEEKDAY = (
        (MONDAY, 'понедельник'),
        (TUESDAY, 'вторник'),
        (WEDNESDAY, 'среда'),
        (THURSDAY, 'четверг'),
        (FRIDAY, 'пятница'),
        (SATURDAY, 'суббота'),
        (SUNDAY, 'воскресенье'),
    )

    EVERY_WEEK = 'EVR'
    ODD_WEEK = 'ODD'
    EVEN_WEEK = 'EVN'

    PERIOD = (
        (EVERY_WEEK, 'еженедельно'),
        (ODD_WEEK, 'нечётные недели'),
        (EVEN_WEEK, 'чётные недели')
    )

    subject = ForeignKey('Subject', on_delete=CASCADE)
    class_type = CharField('тип занятия', max_length=3, choices=CLASS_TYPES)
    teacher = ForeignKey('Teacher', on_delete=DO_NOTHING, blank=True, null=True, verbose_name='преподаватель')
    weekday = CharField('день недели', max_length=3, choices=WEEKDAY)
    period = CharField('период', max_length=3, choices=PERIOD)
    number = IntegerField('номер занятие')

    class Meta:
        verbose_name = 'занятие дисциплины'
        verbose_name_plural = 'занятия дисциплин'


class StudentGroup(Model):
    """ Учебная группа """

    SPECIALIST = 'SPC'
    BACHELOR = 'BAC'
    MAGISTER = 'MAG'

    QUALIFICATION = (
        (SPECIALIST, 'специалитет'),
        (BACHELOR, 'бакалавриат'),
        (MAGISTER, 'магистратура')
    )

    FULL_TIME = 'OC'
    DISTANCE = 'ZA'

    FORM = (
        (FULL_TIME, 'очная'),
        (DISTANCE, 'заочная')
    )

    name = CharField('наименование', max_length=30)
    year = IntegerField('год поступления')
    qualification = CharField('квалификация', max_length=3, choices=QUALIFICATION)
    form = CharField('форма обучения', max_length=2, choices=FORM)

    class Meta:
        verbose_name = 'учебная группа'
        verbose_name_plural = 'учебные группы'
        ordering = ['year', 'name']

    def __str__(self):
        return self.name

    def get_education_duration(self):
        """ Длительность обучения в семестрах """
        answer = 0
        if self.form == StudentGroup.FULL_TIME:
            if self.qualification == StudentGroup.SPECIALIST:
                answer = 10  # очный специалитет, 5 лет
            elif self.qualification == StudentGroup.BACHELOR:
                answer = 8  # очный бакалавриат, 4 года
            elif self.qualification == StudentGroup.MAGISTER:
                answer = 4  # очная магистратура, 2 года
        elif self.form == StudentGroup.DISTANCE:
            if self.qualification == StudentGroup.SPECIALIST:
                answer = 12  # заочный специалитет, 6 лет
            elif self.qualification == StudentGroup.BACHELOR:
                answer = 10  # заочный бакалавриат, 5 лет
            elif self.qualification == StudentGroup.MAGISTER:
                answer = 5  # заочная магистратура, 2,5 года
        return answer

    def get_semester(self, date):
        """ Номер курса """
        half = 0 if date.month < 7 else 1
        return (date.year - self.year) * 2 + half

    def get_course(self, date=None):
        """ Номер курса """
        if date is None:
            date = datetime.now()
        semester = self.get_semester(date)
        answer = '%d курс' % (semester // 2)
        if semester > self.get_education_duration():
            answer = 'обучение завершено'
        elif semester < 0:
            answer = 'обучение не начато'
        return answer


class Room(Model):
    """ Аудитория """

    number = CharField('номер', max_length=50)
    building = CharField('здание', max_length=50)

    class Meta:
        verbose_name = 'аудитория'
        verbose_name_plural = 'аудитории'
        ordering = ['building', 'number']

    def __str__(self):
        return '%s, ауд. %s' % (self.building, self.number)


class Teacher(Model):
    """ Преподаватель """

    last_name = CharField('фамилия', max_length=50)
    first_name = CharField('имя', max_length=50)
    second_name = CharField('отчество', max_length=50, blank=True, default='')
    user = OneToOneField('auth.User', on_delete=DO_NOTHING, blank=True, null=True)

    class Meta:
        verbose_name = 'преподаватель'
        verbose_name_plural = 'преподаватели'
        ordering = ['last_name', 'first_name', 'second_name']

    def __str__(self):
        return '%s %s %s' % (self.last_name, self.first_name, self.second_name)


class Event(Model):
    """ Событие """

    discipline = ForeignKey('Subject', on_delete=CASCADE, blank=True, null=True, verbose_name='дисциплина')
    room = ForeignKey('Room', on_delete=CASCADE, verbose_name='аудитория')
    teacher = ForeignKey('Teacher', on_delete=CASCADE, blank=True, null=True, verbose_name='преподаватель')
    begin = DateTimeField('начало')
    end = DateTimeField('окончание')
    event_type = CharField('тип события', max_length=30)
    description = TextField('описание')

    class Meta:
        verbose_name = 'событие'
        verbose_name_plural = 'события'


class Semester(Model):
    """ График учебного процесса """

    AUTUMN = 'AUT'
    SPRING = 'SPR'

    SEMESTER = (
        (AUTUMN, 'осень'),
        (SPRING, 'весна')
    )

    student_group = ForeignKey('StudentGroup', on_delete=CASCADE, verbose_name='учебная группа')
    year = IntegerField('календарный год')
    semester = CharField('семестр', max_length=3, choices=SEMESTER)
    begin_study = DateField('начало теоретического обучения')
    end_study = DateField('конец теоретического обучения')
    begin_exams = DateField('начало экзаменационной сессии')
    end_exams = DateField('конец экзаменационной сессии')

    class Meta:
        verbose_name = 'семестр'
        verbose_name_plural = 'график учебного процесса'

    def __str__(self):
        begin = self.year
        end = self.year + 1
        if self.semester == Semester.SPRING:
            begin = self.year - 1
            end = self.year
        return '%s: %d-%d, %s' % (self.student_group.name, begin, end, self.get_semester_display())

    def get_study_period(self):
        return '%s – %s­' % (self.begin_study.strftime('%Y.%m.%d'), self.end_study.strftime('%Y.%m.%d'))

    def get_exams_period(self):
        return '%s – %s­' % (self.begin_exams.strftime('%Y.%m.%d'), self.end_exams.strftime('%Y.%m.%d'))

    def get_semester(self):
        begin = self.year
        end = self.year + 1
        if self.semester == Semester.SPRING:
            begin = self.year - 1
            end = self.year
        return '%d-%d уч.г., %s' % (begin, end, self.get_semester_display())

    def get_year_display(self):
        begin = self.year
        end = self.year + 1
        if self.semester == Semester.SPRING:
            begin = self.year - 1
            end = self.year
        return '%d-%d учебный год' % (begin, end)
