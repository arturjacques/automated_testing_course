from models.store import StoreModel
from models.user import UserModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_request = client.post('/auth',
                                           data=json.dumps({'username': 'test', 'password': '1234'}),
                                           headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = f'JWT {auth_token}'

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test')
                self.assertEqual(401, resp.status_code)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('batata', 2.00, 1).save_to_db()
                resp = client.get('/item/batata', headers={'Authorization': self.access_token})
                self.assertDictEqual({'name': 'batata', 'price': 2.00}, json.loads(resp.data))

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('batata', 2.00, 1).save_to_db()

                resp = client.delete('item/batata')
                self.assertEqual(200, resp.status_code)
                self.assertDictEqual({'message': 'Item deleted'}, json.loads(resp.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                resp = client.post('item/batata', data={'price': 2.00, 'store_id': 1})
                self.assertEqual(201, resp.status_code)
                self.assertDictEqual({'name': 'batata', 'price': 2.00}, json.loads(resp.data))
                self.assertIsNotNone(ItemModel.find_by_name('batata'))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                client.post('item/batata', data={'price': 2.00, 'store_id': 1})
                resp = client.post('item/batata', data={'price': 2.00, 'store_id': 1})

                self.assertEqual(400, resp.status_code)
                self.assertEqual({'message': "An item with name 'batata' already exists."}, json.loads(resp.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                resp = client.put('item/batata', data={'price': 2.00, 'store_id': 1})
                self.assertEqual(200, resp.status_code)
                self.assertDictEqual({'name': 'batata', 'price': 2.00}, json.loads(resp.data))
                self.assertIsNotNone(ItemModel.find_by_name('batata'))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('batata', 2.00, 1)
                resp = client.put('item/batata', data={'price': 1.50, 'store_id': 1})
                self.assertEqual(200, resp.status_code)
                self.assertEqual(ItemModel.find_by_name('batata').price, 1.50)
                self.assertDictEqual({'name': 'test', 'price': 1.50}, json.loads(resp.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('batata', 2.00, 1).save_to_db()
                ItemModel('polenta', 5.00, 1).save_to_db()

                expected = {
                    'items':[
                        {
                            'name': 'batata',
                            'price': 2.00
                        },
                        {
                            'name': 'polenta',
                            'price': 5.00
                        }
                    ]
                }

                resp = client.get('/items')
                self.assertEqual(200, resp.status_code)
                self.assertDictEqual(expected, json.loads(resp.data))