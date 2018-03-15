import datetime

from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404, redirect

from schedule_editor import models, forms


def index(request):
    return render(request, "schedule_editor/menu.html", {})


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


def subject_list_page(request, group_id):
    """ Страница списка дисциплин """
    group = get_object_or_404(models.StudentGroup, pk=group_id)
    subjects = list(models.Subject.objects.filter(semester__student_group=group))
    semesters = [{
        'semester': s,
        'subjects': list(filter(lambda subj: subj.semester == s, subjects))
    } for s in models.Semester.objects.filter(student_group=group)]
    if request.method == 'POST':
        subject = get_object_or_404(models.Subject, pk=request.POST.get('subject'))
        subject.delete()
    return render(request, "schedule_editor/subject_list.html", {
        'group': group,
        'semesters': semesters
    })


def subject_update_page(request, subject_id=None):
    """ Страница создания / редактирования дисциплины """
    subject = None if subject_id is None else get_object_or_404(models.Subject, pk=subject_id)
    if request.method == 'POST':
        form = forms.SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    else:
        form = forms.SubjectForm(instance=subject)
    return render(request, 'schedule_editor/subject_form.html', {'form': form, 'subject': subject})


def teacher_list_page(request):
    """ Страница списка преподавателей """
    if request.method == 'POST':
        teacher = get_object_or_404(models.Teacher, pk=request.POST.get('teacher'))
        teacher.delete()
    return render(request, "schedule_editor/teacher_list.html", {
        'teacher_list': models.Teacher.objects.all()
    })


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


def room_list_page(request):
    """ Страница списка дисциплин """
    if request.method == 'POST':
        room = get_object_or_404(models.Room, pk=request.POST.get('room'))
        room.delete()
    return render(request, "schedule_editor/room_list.html", {
        'room_list': models.Room.objects.all()
    })


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


def group_list_page(request):
    """ Страница списка учебных групп """
    if request.method == 'POST':
        student_group = get_object_or_404(models.StudentGroup, pk=request.POST.get('student_group'))
        student_group.delete()
    return render(request, "schedule_editor/group_list.html", {
        'student_group_list': models.StudentGroup.objects.all()
    })


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


def semester_list_page(request):
    """ Страница графика учебного процесса """
    if request.method == 'POST':
        semester = get_object_or_404(models.Semester, pk=request.POST.get('semester'))
        semester.delete()
    return render(request, "schedule_editor/semester_list.html", {
        'semester_list': models.Semester.objects.all()
    })


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
