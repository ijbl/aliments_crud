import json
import random
import string
from rest_framework import status
from rest_framework.test import APITestCase

class AlimentViewTests(APITestCase):

    def _random_string(self,
                       length = 10):
        """
        Generates a random string of a specified length using
        uppercase letters, lowercase letters, and digits.
        """
        characters = string.ascii_letters + string.digits
        random.seed()
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string

    def _new_aliment(self):
        """
        Create a new aliment register invoking the /api/aliments/ API
        """
        request = {
            'name': self._random_string(),
            'description': self._random_string(),
            'status': random.choice([True, False]),
        }
        response = self.client.put('/api/aliments/',
                                   data=json.dumps(request),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return (request, response)

    def assertAliment(self, aliment1, aliment2):
        '''
        Test the equality of two Aliments
        '''
        self.assertEqual(aliment1['name'], aliment2['name'])
        self.assertEqual(aliment1['description'], aliment2['description'])
        self.assertEqual(aliment1['status'], aliment2['status'])

    def assertAlimentExists(self, aliment):
        '''
        Test if an Aliment is already registered
        '''
        response = self.client.get('/api/aliments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        aliments = response.json()
        found_aliments = list(filter(lambda a: a['id'] == aliment['id'], aliments))
        self.assertEqual(len(found_aliments), 1)
        self.assertAliment(aliment, found_aliments[0])

class CreateAlimentViewTests(AlimentViewTests):

    def test_create_aliment(self):
        '''
        Test creating an Aliment with valid data.
        '''
        request, response = self._new_aliment()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertGreater(data['id'], 0)
        self.assertAliment(data, request)

    def test_create_aliment_consecutive_ids(self):
        '''
        Test creating two Aliments resulting in consecutive id's.
        '''
        _, rs1 = self._new_aliment()
        _, rs2 = self._new_aliment()
        self.assertEqual(rs1.json()['id'] + 1, rs2.json()['id'])

    def test_create_aliment_with_empty_name(self):
        '''
        Test creating an Aliment with empty name.
        '''
        aliment = {
            'name': '',
            'description': self._random_string(),
            'status': False,
        }
        response = self.client.put('/api/aliments/',
                                   data=json.dumps(aliment),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_aliment_with_no_name(self):
        '''
        Test creating an Aliment with the name parameter missing.
        '''
        aliment = {
            'description': self._random_string(),
            'status': False,
        }
        response = self.client.put('/api/aliments/',
                                   data=json.dumps(aliment),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_aliment_with_long_name(self):
        '''
        Test creating a name whose length exceeds the maximum allowed.
        '''
        aliment = {
            'name': self._random_string(256),
            'description': self._random_string(),
            'status': False,
        }
        response = self.client.put('/api/aliments/',
                                   data=json.dumps(aliment),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_aliment_with_empty_description(self):
        '''
        Test creating an Aliment with empty description.
        '''
        aliment = {
            'name': self._random_string(),
            'description': '',
            'status': False,
        }
        response = self.client.put('/api/aliments/',
                                   data=json.dumps(aliment),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertGreater(data['id'], 0)
        self.assertAliment(data, aliment)

    def test_create_aliment_with_no_description(self):
        '''
        Test creating an Aliment with the description parameter missing.
        '''
        aliment = {
            'name': self._random_string(),
            'status': False,
        }
        response = self.client.put('/api/aliments/',
                                   data=json.dumps(aliment),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_aliment_with_no_status(self):
        '''
        Test creating an Aliment with status parameter missing.
        '''
        aliment = {
            'name': self._random_string(),
            'description': self._random_string(),
        }
        response = self.client.put('/api/aliments/',
                                   data=json.dumps(aliment),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_aliment_with_invalid_status(self):
        '''
        Test creating an Aliment with the status parameter invalid.
        '''
        aliment = {
            'name': self._random_string(),
            'description': self._random_string(),
            'status': 123,
        }
        response = self.client.put('/api/aliments/',
                                   data=json.dumps(aliment),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class ListAlimentViewTests(AlimentViewTests):

    def test_list_aliments(self):
        '''
        Test listing a previous created Aliment.
        '''
        _, aliment_rs = self._new_aliment()
        aliment = aliment_rs.json()
        self.assertAlimentExists(aliment)

    def test_read_unexistent_aliment(self):
        '''
        Test reading an unexistent aliment.
        '''
        _, aliment_rs = self._new_aliment()
        aliment_id = aliment_rs.json()['id'] + 1
        response = self.client.get(f'/api/aliments/{aliment_id}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class UpdateReadAlimentViewTests(AlimentViewTests):

    def test_update_read_aliment(self):
        '''
        Test updating an Aliment
        '''
        _, aliment_rs = self._new_aliment()
        aliment_id = aliment_rs.json()['id']
        updated_aliment = {
            'name': self._random_string(),
            'description': self._random_string(),
            'status': random.choice([True, False]),
        }
        response = self.client.put(f'/api/aliments/{aliment_id}',
                                   data=json.dumps(updated_aliment),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(f'/api/aliments/{aliment_id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        readed_aliment = response.json()
        self.assertEqual(aliment_id, readed_aliment['id'])
        self.assertAliment(updated_aliment, readed_aliment)

    def test_update_unexistent_aliment(self):
        '''
        Test updating an unexistent aliment.
        '''
        _, aliment_rs = self._new_aliment()
        aliment_id = aliment_rs.json()['id'] + 1
        updated_aliment = {
            'name': self._random_string(),
            'description': self._random_string(),
            'status': random.choice([True, False]),
        }
        response = self.client.put(f'/api/aliments/{aliment_id}',
                                   data=json.dumps(updated_aliment),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class DeleteAlimentViewTest(AlimentViewTests):

    def test_delete_aliment(self):
        '''
        Test deleting an Aliment
        '''
        _, aliment_rs = self._new_aliment()
        aliment = aliment_rs.json()
        self.assertAlimentExists(aliment)
        aliment_id = aliment['id']
        response = self.client.delete(f'/api/aliments/{aliment_id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(AssertionError):
            self.assertAlimentExists(aliment)

    def test_delete_unexistent_aliment(self):
        '''
        Test deleting an unexistent aliment.
        '''
        '''
        Test updating an unexistent aliment.
        '''
        _, aliment_rs = self._new_aliment()
        aliment_id = aliment_rs.json()['id'] + 1
        response = self.client.delete(f'/api/aliments/{aliment_id}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)