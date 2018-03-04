from django.test import Client, TestCase


class TestIndexPage(TestCase):
    """ Проверка """

    def test_index_page(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
