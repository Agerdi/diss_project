from datetime import datetime

from django.test import Client, TestCase

from schedule_editor import models


class TestSubject(TestCase):
    """ Проверка учебных аудиторий """

    def setUp(self):
        """ Начальные данные """
        self.student_group = models.StudentGroup()
        self.student_group.name = 'М-ФИИТ-16'
        self.student_group.year = 2016
        self.student_group.save()

        self.semester1 = models.Semester()
        self.semester1.student_group = self.student_group
        self.semester1.year = 2018
        self.semester1.semester = models.Semester.SPRING
        self.semester1.begin_study = datetime(2018, 2, 2)
        self.semester1.end_study = datetime(2018, 4, 9)
        self.semester1.begin_exams = datetime(2018, 4, 10)
        self.semester1.end_exams = datetime(2018, 4, 16)
        self.semester1.save()

        self.semester2 = models.Semester()
        self.semester2.student_group = self.student_group
        self.semester2.year = 2017
        self.semester2.semester = models.Semester.AUTUMN
        self.semester2.begin_study = datetime(2017, 10, 13)
        self.semester2.end_study = datetime(2018, 1, 18)
        self.semester2.begin_exams = datetime(2018, 1, 19)
        self.semester2.end_exams = datetime(2018, 1, 25)
        self.semester2.save()

        self.subject = models.Subject()
        self.subject.name = 'Математический анализ'
        self.subject.semester = self.semester1
        self.subject.save()

    def test_subject_list_page(self):
        client = Client()
        response = client.get('/subject/list/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Список дисциплин')
        self.assertContains(response, 'Математический анализ')

    def test_subject_edit_page(self):
        client = Client()
        response = client.get('/subject/update/%d/' % self.subject.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Редактирование дисциплины')
        self.assertContains(response, 'Математический анализ')
        self.assertContains(response, 'М-ФИИТ-16')
        self.assertContains(response, '2018')
        self.assertContains(response, 'весенний')

        response = client.post('/subject/update/%d/' % self.subject.id, {
            'name': 'Дифференциальные уравнения',
            'semester': self.semester2.id
        })
        self.assertEqual(response.status_code, 302)

        response = client.get('/subject/list/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Список дисциплин')
        self.assertNotContains(response, 'Математический анализ')
        self.assertContains(response, 'Дифференциальные уравнения')

    def test_subject_create_page(self):
        client = Client()
        response = client.get('/subject/create/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Редактирование дисциплины')

        response = client.post('/subject/create/', {
            'name': 'Дифференциальные уравнения',
            'semester': self.semester2.id
        })
        self.assertEqual(response.status_code, 302)

        response = client.get('/subject/list/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Список дисциплин')
        self.assertContains(response, 'Математический анализ')
        self.assertContains(response, 'Дифференциальные уравнения')
