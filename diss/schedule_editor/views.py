import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404, redirect

from . import models, forms


# from icalendar import Calendar, Event, vRecur


def index(request):
    return render(request, "schedule_editor/menu.html", {})


def login_page(request):
    """ Страница входа в систему """
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is None:
                form.add_error(None, 'Неправильный логин или пароль')
            else:
                login(request, user)
                return redirect('index')
    else:
        form = forms.LoginForm()
    return render(request, 'schedule_editor/login.html', {'form': form})


def logout_page(request):
    logout(request)
    return redirect('index')


@login_required
def subject_group_page(request):
    """ Страница графика учебного процесса """
    group_list = [{
        'qualification': g.get_qualification_display(),
        'course': g.get_course(),
        'group': g
    } for g in models.StudentGroup.objects.all()]
    group_list = list(filter(lambda g: g['course'] != 'обучение не начато', group_list))
    group_list = list(filter(lambda g: g['course'] != 'обучение завершено', group_list))
    group_list.sort(key=lambda g: (g['qualification'], g['course']))
    return render(request, "schedule_editor/subject_group.html", {
        'group_list': group_list
    })


@login_required
def subject_list_page(request, group_id):
    """ Страница списка дисциплин учебной группы """

    # При необходимости, удалим дисциплину
    if request.method == 'POST':
        subject = get_object_or_404(models.Subject, pk=request.POST.get('subject'))
        subject.delete()

    # Найдем учебную группу
    group = get_object_or_404(models.StudentGroup, pk=group_id)

    # Получим семестры
    semesters = [{'semester': sem} for sem in models.Semester.objects.filter(student_group=group)]

    # Получим данные дисциплин
    subjects = list(models.Subject.objects.select_related('semester').filter(semester__student_group=group))

    # Получим данные занятий дисциплин
    subject_classes = list(models.SubjectClass.objects.select_related('subject__semester')
                           .filter(subject__semester__student_group=group))

    for sem in semesters:
        sem['subjects'] = [{'subject': sbj} for sbj in subjects if sbj.semester == sem['semester']]

        for sbj in sem['subjects']:
            sbj['lecture_hours'] = 0
            sbj['lab_work_hours'] = 0
            sbj['practice_hours'] = 0
            sbj['total_hours'] = sbj['subject'].student_work_hours + sbj['subject'].control_hours
            for sc in subject_classes:
                if sc.subject == sbj['subject']:
                    hours = sc.get_count() * 2
                    if sc.class_type == models.SubjectClass.LECTURE:
                        sbj['lecture_hours'] += hours
                    if sc.class_type == models.SubjectClass.LAB_WORK:
                        sbj['lab_work_hours'] += hours
                    if sc.class_type == models.SubjectClass.PRACTICE:
                        sbj['practice_hours'] += hours
                    sbj['total_hours'] += hours

    return render(request, "schedule_editor/subject_list.html", {
        'group': group,
        'semesters': semesters
    })


@login_required
def subject_update_page(request, group_id, subject_id=None):
    """ Страница создания / редактирования дисциплины """
    group = get_object_or_404(models.StudentGroup, pk=group_id)
    subject = None if subject_id is None else get_object_or_404(models.Subject, pk=subject_id)
    if request.method == 'POST':
        form = forms.SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('subject_list', group_id=group.id)
    else:
        form = forms.SubjectForm(instance=subject)
    return render(request, 'schedule_editor/subject_form.html', {'form': form, 'subject': subject, 'group': group})


def subject_class_page(request, subject_id, class_id=None):
    """ Редактирование занятия дисциплины """
    subject = get_object_or_404(models.Subject, pk=subject_id)
    group = subject.semester.student_group
    subject_class = None if class_id is None else get_object_or_404(models.SubjectClass, pk=class_id)
    if request.method == 'POST':
        form = forms.SubjectClassForm(request.POST, instance=subject_class)
        if form.is_valid():
            form.save()
            return redirect('subject_update', group_id=group.id, subject_id=subject.id)
    else:
        form = forms.SubjectClassForm(instance=subject_class)
    return render(request, 'schedule_editor/subject_class.html', {'form': form, 'subject': subject, 'group': group})


def subject_class_delete(request, subject_id, class_id):
    """ Удаление занятия дисциплины """
    subject_class = get_object_or_404(models.SubjectClass, pk=class_id)
    subject_class.delete()
    subject = get_object_or_404(models.Subject, pk=subject_id)
    semester = subject.semester
    student_group = semester.student_group
    return redirect('subject_update', student_group.id, subject.id)


@login_required
def teacher_list_page(request):
    """ Страница списка преподавателей """
    if request.method == 'POST':
        teacher = get_object_or_404(models.Teacher, pk=request.POST.get('teacher'))
        teacher.delete()
    return render(request, "schedule_editor/teacher_list.html", {
        'teacher_list': models.Teacher.objects.all()
    })


@login_required
def teacher_update_page(request, teacher_id=None):
    """ Страница создания / редактирования преподавателя """
    teacher = None if teacher_id is None else get_object_or_404(models.Teacher, pk=teacher_id)
    if request.method == 'POST':
        form = forms.TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher_list')
    else:
        form = forms.TeacherForm(instance=teacher)
    return render(request, 'schedule_editor/teacher_form.html', {'form': form, 'teacher': teacher})


@login_required
def room_list_page(request):
    """ Страница списка дисциплин """
    if request.method == 'POST':
        room = get_object_or_404(models.Room, pk=request.POST.get('room'))
        room.delete()
    return render(request, "schedule_editor/room_list.html", {
        'room_list': models.Room.objects.all()
    })


@login_required
def room_update_page(request, room_id=None):
    """ Страница создания / редактирования дисциплины """
    room = None if room_id is None else get_object_or_404(models.Room, pk=room_id)
    if request.method == 'POST':
        form = forms.RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = forms.RoomForm(instance=room)
    return render(request, 'schedule_editor/room_form.html', {'form': form, 'room': room})


@login_required
def group_list_page(request):
    """ Страница списка учебных групп """
    if request.method == 'POST':
        student_group = get_object_or_404(models.StudentGroup, pk=request.POST.get('student_group'))
        student_group.delete()
    return render(request, "schedule_editor/group_list.html", {
        'student_group_list': models.StudentGroup.objects.all()
    })


@login_required
def group_update_page(request, group_id=None):
    """ Страница создания / редактирования учебных групп """
    student_group = None if group_id is None else get_object_or_404(models.StudentGroup, pk=group_id)
    if request.method == 'POST':
        form = forms.StudentGroupForm(request.POST, instance=student_group)
        if form.is_valid():
            form.save()
            return redirect('group_list')
    else:
        form = forms.StudentGroupForm(instance=student_group)
    return render(request, 'schedule_editor/group_form.html', {'form': form, 'student_group': student_group})


@login_required
def semester_list_page(request):
    """ Страница графика учебного процесса """
    if request.method == 'POST':
        semester = get_object_or_404(models.Semester, pk=request.POST.get('semester'))
        semester.delete()
    return render(request, "schedule_editor/semester_list.html", {
        'semester_list': models.Semester.objects.all()
    })


@login_required
def semester_update_page(request, semester_id=None):
    """ Страница создания / редактирования семестра """
    semester = None if semester_id is None else get_object_or_404(models.Semester, pk=semester_id)
    if request.method == 'POST':
        form = forms.SemesterForm(request.POST, instance=semester)
        if form.is_valid():
            form.save()
            return redirect('semester_list')
    else:
        form = forms.SemesterForm(instance=semester)
    return render(request, 'schedule_editor/semester_form.html', {'form': form, 'semester': semester})


@login_required
def week(request, year, month, day, group_id=None):
    year, month, day = int(year), int(month), int(day)
    request.session['year'] = year
    request.session['month'] = month
    request.session['day'] = day
    start = datetime.datetime(year, month, day)
    start -= datetime.timedelta(days=start.weekday())
    end = start + datetime.timedelta(days=7)
    if group_id is None:
        events = models.Event.objects.filter(begin__gte=start, end__lt=end)
    # else:
        # events = models.Event.objects.filter(begin__gte=start, end__lt=end, participants=group_id)
    return render(request, 'schedule_editor/week.html', {
        'start': start,
        'prev_week': start - datetime.timedelta(days=7),
        'next_week': start + datetime.timedelta(days=7),
        'events': events,
        'group': None if group_id is None else Group.objects.get(pk=group_id),
        'groups': Group.objects.all(),
    })


#------Экспорт в iCal---------
# def test_page(request, event_id):
#     timezone.activate(pytz.timezone(request.user.timezone))
#     instance = get_object_or_404(models.Event, id=event_id)
#
#     event = Event()
#     event.add =('Summary', instance.summary)
#     event.add =('uid', UUID(int=5))
#     event.add =('dtStart', instance.start)
#     event.add =('dtEnd', instance.end)
#     event.add =('dtStamp', instance.start)
#     if instance.period is not None:
#         event.add('rRule', vRecur(freq=instance.period, interval=instance.interval))
#     event.add =('Location', instance.location)
#     event.add =('Description', instance.description)
#
#     cal = Calendar()
#     cal.add('Version','2.0')
#     cal.add('ProdId','-//KIT IMI//Project Arcadia//')
#     cal.add_component(event)
#
#     return HttpResponse(cal.to_ical(), content_type='plain/calendar')
