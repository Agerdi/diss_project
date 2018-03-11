from django.test import Client, TestCase

from schedule_editor import models


class TestTeacher(TestCase):
    """ Проверка преподавателей """

    def setUp(self):
        """ Начальные данные """
        self.teacher = models.Teacher()
        self.teacher.last_name = 'Иванов'
        self.teacher.first_name = 'Иван'
        self.teacher.second_name = 'Иванович'
        self.teacher.save()

    def test_teacher_list_page(self):
        client = Client()
        response = client.get('/teacher/list/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Преподаватели')
        self.assertContains(response, 'Иванов Иван Иванович')

    def test_teacher_edit_page(self):
        client = Client()
        response = client.get('/teacher/update/%d/' % self.teacher.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Редактирование преподавателя')
        self.assertContains(response, 'Иванов')
        self.assertContains(response, 'Иван')
        self.assertContains(response, 'Иванович')

        response = client.post('/teacher/update/%d/' % self.teacher.id, {
            'last_name': 'Петров',
            'first_name': 'Петр',
            'second_name': 'Петрович'
        })
        self.assertEqual(response.status_code, 302)

        response = client.get('/teacher/list/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Преподаватели')
        self.assertNotContains(response, 'Иванов Иван Иванович')
        self.assertContains(response, 'Петров Петр Петрович')

    def test_teacher_create_page(self):
        client = Client()
        response = client.get('/teacher/create/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Редактирование преподавателя')

        response = client.post('/teacher/create/', {
            'last_name': 'Петров',
            'first_name': 'Петр',
            'second_name': 'Петрович'
        })
        self.assertEqual(response.status_code, 302)

        response = client.get('/teacher/list/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Преподаватели')
        self.assertContains(response, 'Иванов Иван Иванович')
        self.assertContains(response, 'Петров Петр Петрович')
