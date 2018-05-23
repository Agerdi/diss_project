from django.shortcuts import render
from . import models
import django_filters


class GroupFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = models.Event()
        fields = ['subject_class__subject__semester__student_group__name']

def student_group_list(request):
    f = GroupFilter(request.GET, queryset=models.StudentGroup.objects.all())
    return render(request, 'schedule_editor/week.html', {'filter': f})
