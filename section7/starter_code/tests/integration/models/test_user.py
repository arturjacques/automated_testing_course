from tests.base_test import BaseTest
from models.user import UserModel


class TestUser(BaseTest):
    def test_save_to_db(self):
        with self.app_context():
            user = UserModel('test_user', '1234')

            self.assertIsNone(user.find_by_username('test_user'))
            self.assertIsNone(user.find_by_id(1))

            user.save_to_db()

            self.assertIsNotNone(user.find_by_username('test_user'))
            self.assertIsNotNone(user.find_by_id(1))