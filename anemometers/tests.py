from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Anemometer, Tag


class AnemometerModelTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username='user',
            password='pass'
        )

        self.client.force_authenticate(user=self.user)

        tag1 = Tag.objects.create(name='tag1')
        tag2 = Tag.objects.create(name='tag2')

        self.anemometer = Anemometer.objects.create(
            name='Anemometer 1',
            coordinates='POINT(12.34 3.78)'
        )
        self.anemometer.tags.set([tag1, tag2])

    def test_anemometer_tags(self):
        self.assertEqual(self.anemometer.tags.count(), 2)
        self.assertEqual(self.anemometer.tags.first().name, 'tag1')

    def test_list_anemometers(self):
        response = self.client.get('/api/anemometers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], 'Anemometer 1')

    def test_create_anemometer(self):
        data = {
            'name': 'Anemometer 2',
            'coordinates': 'POINT(12.34 3.78)',
            'tags': ['tag1', 'tag2']
        }
        response = self.client.post('/api/anemometers/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Anemometer.objects.count(), 2)
        self.assertEqual(Anemometer.objects.get(
            pk=response.json()['id']).name, 'Anemometer 2')
