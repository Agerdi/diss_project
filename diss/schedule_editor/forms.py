from django import forms

from . import models


class LoginForm(forms.Form):
    """ Форма входа в систему """
    username = forms.CharField(max_length=150, label='Логин')
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')


class SubjectForm(forms.ModelForm):
    """ Форма редактирования задачи """
    class Meta:
        fields = [
            'name', 'semester',
            'lecture_hours', 'lab_work_hours', 'practice_hours',
            'student_work_hours', 'control_hours', 'total_hours'
        ]
        model = models.Subject


class SubjectClassForm(forms.ModelForm):
    """ Форма редактирования занятия дистанции """
    class Meta:
        fields = ['subject', 'class_type', 'weekday', 'number', 'period', 'teacher']
        model = models.SubjectClass


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
        fields = ['name', 'year', 'form', 'qualification']
        model = models.StudentGroup


class SemesterForm(forms.ModelForm):
    """ Форма редактирования семестра """
    class Meta:
        fields = ['student_group', 'year', 'semester', 'begin_study', 'end_study', 'begin_exams', 'end_exams']
        model = models.Semester
