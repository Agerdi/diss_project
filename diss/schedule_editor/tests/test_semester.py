from datetime import datetime

from django.test import Client, TestCase

from schedule_editor import models


class TestSemester(TestCase):
    """ Проверка графика учебного процесса """

    def setUp(self):
        """ Начальные данные """
        self.group = models.StudentGroup()
        self.group.name = 'М-ФИИТ-16'
        self.group.year = 2016
        self.group.save()

        self.semester = models.Semester()
        self.semester.student_group = self.group
        self.semester.year = 2017
        self.semester.semester = models.Semester.AUTUMN
        self.semester.begin_study = datetime(2017, 10, 13)
        self.semester.end_study = datetime(2018, 1, 18)
        self.semester.begin_exams = datetime(2018, 1, 19)
        self.semester.end_exams = datetime(2018, 1, 25)
        self.semester.save()

    def test_semester_list_page(self):
        client = Client()
        response = client.get('/semester/list/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'График учебного процесса')
        self.assertContains(response, 'М-ФИИТ-16: 2017-2018 учебный год, осенний семестр')

    def test_semester_edit_page(self):
        client = Client()
        response = client.get('/semester/update/%d/' % self.semester.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Редактирование семестра')
        self.assertContains(response, 'М-ФИИТ-16')
        self.assertContains(response, 'осенний')
        self.assertContains(response, '13.10.2017')
        self.assertContains(response, '18.01.2018')
        self.assertContains(response, '19.01.2018')
        self.assertContains(response, '25.01.2018')

        response = client.post('/semester/update/%d/' % self.semester.id, {
            'student_group': self.group.id,
            'year': 2018,
            'semester': models.Semester.SPRING,
            'begin_study': '09.02.2018',
            'end_study': '28.04.2018',
            'begin_exams': '29.04.2018',
            'end_exams': '03.05.2018'
        })
        self.assertEqual(response.status_code, 302)

        response = client.get('/semester/list/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'График учебного процесса')
        self.assertNotContains(response, 'М-ФИИТ-16: 2017-2018 учебный год, осенний семестр')
        self.assertContains(response, 'М-ФИИТ-16: 2017-2018 учебный год, весенний семестр')

    def test_semester_create_page(self):
        client = Client()
        response = client.get('/semester/create/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Редактирование семестра')

        response = client.post('/semester/create/', {
            'student_group': self.group.id,
            'year': 2018,
            'semester': models.Semester.SPRING,
            'begin_study': '09.02.2018',
            'end_study': '28.04.2018',
            'begin_exams': '29.04.2018',
            'end_exams': '03.05.2018'
        })
        self.assertEqual(response.status_code, 302)

        response = client.get('/semester/list/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'График учебного процесса')
        self.assertContains(response, 'М-ФИИТ-16: 2017-2018 учебный год, осенний семестр')
        self.assertContains(response, 'М-ФИИТ-16: 2017-2018 учебный год, весенний семестр')
