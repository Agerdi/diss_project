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

        self.subject = models.Subject()
        self.subject.name = 'Математический анализ'
        self.subject.student_group = self.student_group
        self.subject.year = 2018
        self.subject.semester = models.SPRING
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
            'student_group': self.student_group.id,
            'year': 2017,
            'semester': models.AUTUMN
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
            'student_group': self.student_group.id,
            'year': 2017,
            'semester': models.AUTUMN
        })
        self.assertEqual(response.status_code, 302)

        response = client.get('/subject/list/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Список дисциплин')
        self.assertContains(response, 'Математический анализ')
        self.assertContains(response, 'Дифференциальные уравнения')
