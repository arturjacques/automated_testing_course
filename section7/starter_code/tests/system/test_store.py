from models.store import StoreModel
from tests.base_test import BaseTest
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/store_test')
                self.assertEqual(201, response.status_code)
                self.assertIsNotNone(StoreModel.find_by_name('store_test'))
                self.assertDictEqual({'name': 'store_test', 'items': []}, json.loads(response.data))

    def test_create_duplicated_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/store_test')
                response = client.post('/store/store_test')

                self.assertEqual(400, response.status_code)
                self.assertDictEqual({'message': "A store with name 'store_test' already exists."},
                                     json.loads(response.data))

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/store_test')

                response_delete = client.delete('/store/store_test')
                self.assertEqual(200, response_delete.status_code)
                self.assertDictEqual({'message': 'Store deleted'}, json.loads(response_delete.data))

                response_get = client.get('/store/store_test')
                self.assertEqual(404, response_get.status_code)

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/store_test')
                response_get = client.get('/store/store_test')
                self.assertEqual(200, response_get.status_code)

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response_get = client.get('/store/store_test')
                self.assertEqual(404, response_get.status_code)
                self.assertDictEqual({'message': 'Store not found'}, json.loads(response_get.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                expected = {
                    'name': 'store_test',
                    'items': [{
                        'name': 'banana',
                        'price': 2.00
                    }]
                }
                client.post('/store/store_test')

                response_put = client.put('/item/banana', data={'price': 2.00, 'store_id': 1})
                self.assertEqual(200, response_put.status_code)

                response_get = client.get('/store/store_test')
                self.assertDictEqual(expected, json.loads(response_get.data))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                expected = {
                    'stores':[
                        {
                            'name': 'store_test',
                            'items': []
                        },
                        {
                            'name': 'store_test_2',
                            'items': []
                        }
                    ]
                }

                client.post('/store/store_test')
                client.post('/store/store_test_2')
                get_response = client.get('/stores')
                self.assertEqual(200, get_response.status_code)
                self.assertDictEqual(expected, json.loads(get_response.data))

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                expected = {
                    'stores':[
                        {
                            'name': 'store_test',
                            'items': [{'name': 'banana', 'price': 2.00}]
                        },
                        {
                            'name': 'store_test_2',
                            'items': [{'name': 'polenta', 'price': 5.00}]
                        }
                    ]
                }

                client.post('/store/store_test')
                client.post('/store/store_test_2')
                client.put('/item/banana', data={'price': 2.00, 'store_id': 1})
                client.put('/item/polenta', data={'price': 5.00, 'store_id': 2})
                get_response = client.get('/stores')
                self.assertEqual(200, get_response.status_code)
                self.assertDictEqual(expected, json.loads(get_response.data))