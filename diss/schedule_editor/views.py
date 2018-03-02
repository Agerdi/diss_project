import datetime

from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404, redirect

from schedule_editor import models, forms


def index(request):
    return render(request, "schedule_editor/menu.html", {})


def subject_list_page(request):
    """ Страница списка дисциплин """
    subject_list = models.Discipline.objects.all()
    return render(request, "schedule_editor/subject_list.html", {
        'subject_list': subject_list
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


def subject_remove_page(request, subject_id):
    subject = get_object_or_404(models.Discipline, pk=subject_id)
    subject.delete()
    return redirect('subject_list')


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
