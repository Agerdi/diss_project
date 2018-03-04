from django.test import Client, TestCase

from schedule_editor import models


class TestRoom(TestCase):
    """ Проверка аудиторий """

    def setUp(self):
        """ Начальные данные """
        self.room = models.Room()
        self.room.building = 'КФЕН'
        self.room.number = '461'
        self.room.save()

    def test_room_list_page(self):
        client = Client()
        response = client.get('/room/list/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Список аудиторий')
        self.assertContains(response, 'КФЕН, ауд. 461')

    def test_room_edit_page(self):
        client = Client()
        response = client.get('/room/update/%d/' % self.room.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Редактирование аудитории')
        self.assertContains(response, 'КФЕН')
        self.assertContains(response, '461')

        response = client.post('/room/update/%d/' % self.room.id, {
            'building': 'КФЕН',
            'number': '437'
        })
        self.assertEqual(response.status_code, 302)

        response = client.get('/room/list/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Список аудиторий')
        self.assertNotContains(response, 'КФЕН, ауд. 461')
        self.assertContains(response, 'КФЕН, ауд. 437')

    def test_room_create_page(self):
        client = Client()
        response = client.get('/room/create/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Редактирование аудитории')

        response = client.post('/room/create/', {
            'building': 'КФЕН',
            'number': '437'
        })
        self.assertEqual(response.status_code, 302)

        response = client.get('/room/list/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Список аудиторий')
        self.assertContains(response, 'КФЕН, ауд. 461')
        self.assertContains(response, 'КФЕН, ауд. 437')
