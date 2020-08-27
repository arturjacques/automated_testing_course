from unittest import TestCase
from blog import Blog


class BlogTest(TestCase):
    def test_create_post(self):
        b = Blog('Test', 'Test Author')
        b.create_post('Test Post', 'Post Content')
        b.create_post('Test Post2', 'Post Content2')

        self.assertEqual(len(b.posts), 2)
        self.assertEqual(b.posts[0].title, 'Test Post')
        self.assertEqual(b.posts[0].content, 'Post Content')
        self.assertEqual(b.posts[1].title, 'Test Post2')
        self.assertEqual(b.posts[1].content, 'Post Content2')

    def test_json_no_posts(self):
        b = Blog('Test', 'Test Author')
        expected = {'title': 'Test', 'author': 'Test Author', 'posts': []}

        self.assertDictEqual(expected, b.json())

    def test_json(self):
        b = Blog('Test', 'Test Author')
        b.create_post('Test Post', 'Post Content')
        b.create_post('Test Post2', 'Post Content2')

        expected = {
            'title': 'Test',
            'author': 'Test Author',
            'posts': [
                {'title': 'Test Post',
                 'content': 'Post Content'},
                {'title': 'Test Post2',
                 'content': 'Post Content2'}
            ]
        }

        self.assertEqual(expected, b.json())
