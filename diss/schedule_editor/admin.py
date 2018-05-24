from django.contrib import admin

from . import models

admin.site.register(models.Teacher)
admin.site.register(models.Event)


@admin.register(models.StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    actions_on_top = False
    list_display = ['name', 'year', 'qualification', 'form']
    list_filter = ['year', 'qualification', 'form']
    search_fields = ['name']


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    actions_on_top = False
    list_display = ['number', 'building', 'computer']
    list_filter = ['building', 'computer']
    search_fields = ['number']


@admin.register(models.Semester)
class SemesterAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    actions_on_top = False
    list_display = ['student_group', 'year', 'semester', 'get_study_period', 'get_exams_period']
    list_filter = ['student_group', 'year', 'semester']


@admin.register(models.Subject)
class CourseAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    actions_on_top = False
    list_display = ['name', 'semester', 'lecture_hours', 'practice_hours', 'lab_work_hours', 'total_hours']
    list_filter = ['semester__student_group', 'semester__year', 'semester__semester']
    search_fields = ['name']


@admin.register(models.SubjectClass)
class CourseClassAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    actions_on_top = False
    list_display = ['subject', 'class_type', 'teacher', 'weekday', 'number', 'period']
    list_filter = ['subject', 'teacher', 'class_type', 'weekday', 'number']
    search_fields = ['course__name']
