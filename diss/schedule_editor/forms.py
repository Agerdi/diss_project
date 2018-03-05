from django import forms

from schedule_editor import models


class SubjectForm(forms.ModelForm):
    """ Форма редактирования задачи """
    class Meta:
        exclude = ['author', 'last_modified']
        model = models.Discipline


class TeacherForm(forms.ModelForm):
    """ Форма редактирования преподавателя """
    class Meta:
        fields = ['last_name', 'first_name', 'second_name', 'user']
        model = models.Teacher


class RoomForm(forms.ModelForm):
    """ Форма редактирования преподавателя """
    class Meta:
        fields = ['number', 'building']
        model = models.Room


class StudentGroupForm(forms.ModelForm):
    """ Форма редактирования учебной группы """
    class Meta:
        fields = ['name', 'year']
        model = models.StudentGroup


class SemesterForm(forms.ModelForm):
    """ Форма редактирования семестра """
    class Meta:
        fields = ['student_group', 'year', 'semester', 'begin_study', 'end_study', 'begin_exams', 'end_exams']
        model = models.Semester
