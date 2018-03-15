from django.test import Client, TestCase

from schedule_editor import models


class TestStudentGroup(TestCase):
    """ Проверка учебных аудиторий """

    def setUp(self):
        """ Начальные данные """
        self.student_group = models.StudentGroup()
        self.student_group.name = 'М-ФИИТ-16'
        self.student_group.year = 2016
        self.student_group.save()

    def test_group_list_page(self):
        client = Client()
        response = client.get('/group/list/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Учебные группы')
        self.assertContains(response, 'М-ФИИТ-16')

    def test_group_edit_page(self):
        client = Client()
        response = client.get('/group/update/%d/' % self.student_group.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Редактирование учебной группы')
        self.assertContains(response, 'М-ФИИТ-16')
        self.assertContains(response, '2016')

        response = client.post('/group/update/%d/' % self.student_group.id, {
            'name': 'М-ИВТ-17',
            'year': 2017,
            'qualification': models.StudentGroup.MAGISTER,
            'form': models.StudentGroup.FULL_TIME
        })
        self.assertEqual(response.status_code, 302)

        response = client.get('/group/list/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Учебные группы')
        self.assertNotContains(response, 'М-ФИИТ-16')
        self.assertContains(response, 'М-ИВТ-17')
        self.assertContains(response, 'магистратура')
        self.assertContains(response, 'очная')

    def test_group_create_page(self):
        client = Client()
        response = client.get('/group/create/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Редактирование учебной группы')

        response = client.post('/group/create/', {
            'name': 'М-ИВТ-17',
            'year': 2017,
            'qualification': models.StudentGroup.MAGISTER,
            'form': models.StudentGroup.FULL_TIME
        })
        self.assertEqual(response.status_code, 302)

        response = client.get('/group/list/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Учебные группы')
        self.assertContains(response, 'М-ФИИТ-16')
        self.assertContains(response, 'М-ИВТ-17')
        self.assertContains(response, 'магистратура')
        self.assertContains(response, 'очная')
