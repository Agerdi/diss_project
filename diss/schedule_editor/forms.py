from django import forms

from schedule_editor import models


class SubjectForm(forms.ModelForm):
    """ Форма редактирования задачи """
    class Meta:
        exclude = ['author', 'last_modified']
        model = models.Discipline
