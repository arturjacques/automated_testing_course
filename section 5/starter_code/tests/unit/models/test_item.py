from unittest import TestCase

from models.item import ItemModel


class TestItemModel(TestCase):
    def setUp(self):
        pass

    def test_create_item(self):
        item = ItemModel('Batata', 2.50)
        self.assertEqual(item.name, 'Batata',
                         'The name of the item after creation not equal the constructor argument')
        self.assertEqual(item.price, 2.50,
                         'The price of the item after creation not equal the constructor argument')

    def test_item_json(self):
        item = ItemModel('Batata', 2.50)
        expected = {
            'name': 'Batata',
            'price': 2.50,
        }
        self.assertEqual(item.json(), expected)

