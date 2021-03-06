from datetime import datetime, timedelta

from django.db.models import (CASCADE, CharField, DateField, DateTimeField, DO_NOTHING, ForeignKey, IntegerField, Model,
                              OneToOneField, TextField, BooleanField)


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


class SubjectClass(Model):
    """ Занятие дисциплины """

    LECTURE = 'LEC'
    LAB_WORK = 'LAB'
    PRACTICE = 'PRA'

    CLASS_TYPES = (
        (LECTURE, 'лекция'),
        (LAB_WORK, 'лабораторная работа'),
        (PRACTICE, 'практическое занятие')
    )

    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    WEEKDAY = (
        (MONDAY, 'понедельник'),
        (TUESDAY, 'вторник'),
        (WEDNESDAY, 'среда'),
        (THURSDAY, 'четверг'),
        (FRIDAY, 'пятница'),
        (SATURDAY, 'суббота'),
        (SUNDAY, 'воскресенье'),
    )

    EVERY_WEEK = -1
    ODD_WEEK = 1
    EVEN_WEEK = 0

    PERIOD = (
        (EVERY_WEEK, 'еженедельно'),
        (ODD_WEEK, 'нечётные недели'),
        (EVEN_WEEK, 'чётные недели')
    )

    subject = ForeignKey('Subject', on_delete=CASCADE, verbose_name='дисциплина')
    class_type = CharField('тип занятия', max_length=3, choices=CLASS_TYPES)
    teacher = ForeignKey('Teacher', on_delete=DO_NOTHING, blank=True, null=True, verbose_name='преподаватель')
    weekday = IntegerField('день недели', choices=WEEKDAY)
    period = IntegerField('период', choices=PERIOD)
    number = IntegerField('номер занятия')

    class Meta:
        verbose_name = 'занятие дисциплины'
        verbose_name_plural = 'занятия дисциплин'

    def get_count(self):
        """ Получить количество повторов """

        semester = self.subject.semester
        begin_study = semester.begin_study
        end_study = semester.end_study

        # День недели перед началом семестра
        cur_day = begin_study - timedelta(days=begin_study.weekday()) + timedelta(days=self.weekday)
        if cur_day >= begin_study:
            cur_day -= timedelta(days=7)

        # Если чётность недели не совпадает, тогда отнимем ещё неделю
        if self.period != SubjectClass.EVERY_WEEK:
            _, week_number, _ = cur_day.isocalendar()
            if week_number % 2 != self.period:
                cur_day -= timedelta(days=7)

        # Периодичность занятий
        delta = timedelta(days=(7 if self.period == SubjectClass.EVERY_WEEK else 14))

        # Подсчёт количества занятий до конца семестра
        count = -1
        while cur_day < end_study:
            cur_day += delta
            count += 1

        return count


class StudentGroup(Model):
    """ Учебная группа """

    SPECIALIST = 'SPC'
    BACHELOR = 'BAC'
    MASTER = 'MAG'

    QUALIFICATION = (
        (SPECIALIST, 'специалитет'),
        (BACHELOR, 'бакалавриат'),
        (MASTER, 'магистратура')
    )

    FULL_TIME = 'OC'
    DISTANCE = 'ZA'

    FORM = (
        (FULL_TIME, 'очная'),
        (DISTANCE, 'заочная')
    )

    name = CharField('наименование', max_length=30, unique=True)
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
            elif self.qualification == StudentGroup.MASTER:
                answer = 4  # очная магистратура, 2 года
        elif self.form == StudentGroup.DISTANCE:
            if self.qualification == StudentGroup.SPECIALIST:
                answer = 12  # заочный специалитет, 6 лет
            elif self.qualification == StudentGroup.BACHELOR:
                answer = 10  # заочный бакалавриат, 5 лет
            elif self.qualification == StudentGroup.MASTER:
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
    computer = BooleanField('компьютерная', default=False)

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

    subject_class = ForeignKey('SubjectClass', on_delete=CASCADE, blank=True, null=True,
                               verbose_name='занятие дисциплины')
    room = ForeignKey('Room', on_delete=DO_NOTHING, verbose_name='аудитория')
    teacher = ForeignKey('Teacher', on_delete=DO_NOTHING, blank=True, null=True, verbose_name='преподаватель')

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
    begin_study = DateField('начало теоретического обучения', blank=True, null=True)
    end_study = DateField('конец теоретического обучения', blank=True, null=True)
    begin_exams = DateField('начало экзаменационной сессии', blank=True, null=True)
    end_exams = DateField('конец экзаменационной сессии', blank=True, null=True)

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
        """ Период обучения """
        if self.begin_study is None or self.end_study is None:
            return ""
        else:
            return '%s – %s' % (self.begin_study.strftime('%Y.%m.%d'), self.end_study.strftime('%Y.%m.%d'))
    get_study_period.short_description = "Период обучения"

    def get_exams_period(self):
        """ Сессия """
        if self.begin_exams is None or self.end_exams is None:
            return ""
        else:
            return '%s – %s' % (self.begin_exams.strftime('%Y.%m.%d'), self.end_exams.strftime('%Y.%m.%d'))
    get_exams_period.short_description = "Сессия"

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
