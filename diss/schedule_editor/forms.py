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
