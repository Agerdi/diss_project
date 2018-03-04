import datetime

from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404, redirect

from schedule_editor import models, forms


def index(request):
    return render(request, "schedule_editor/menu.html", {})


def subject_list_page(request):
    """ Страница списка дисциплин """
    if request.method == 'POST':
        subject = get_object_or_404(models.Discipline, pk=request.POST.get('subject'))
        subject.delete()
    return render(request, "schedule_editor/subject_list.html", {
        'subject_list': models.Discipline.objects.all()
    })


def subject_update_page(request, subject_id=None):
    """ Страница создания / редактирования дисциплины """
    subject = None if subject_id is None else get_object_or_404(models.Discipline, pk=subject_id)
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
