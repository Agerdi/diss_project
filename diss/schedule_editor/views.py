import datetime
from django.shortcuts import render
from django.contrib.auth.models import Group
from schedule_editor import models


def index(request):
    return render(request, "schedule_editor/menu.html", {})


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
