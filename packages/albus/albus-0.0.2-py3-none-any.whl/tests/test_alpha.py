from unittest import TestCase

from albus.field import IntegerField, StringField
from albus.model import Model


class NoFieldsModelTest(TestCase):

    def setUp(self):
        class FooModel(Model):
            pass

        self.FooModel = FooModel

    def test_new_model(self):
        new = self.FooModel()
        self.assertIsNotNone(new)

    def test_to_json(self):
        new = self.FooModel()
        got = new.to_json()
        expected = {'id': None}
        self.assertEqual(got, expected)


class SimpleModelTest(TestCase):

    def setUp(self):
        class Book(Model):
            title = StringField()
            rank = IntegerField()

        self.Book = Book

    def test_new_model(self):
        book = self.Book()
        self.assertIsNotNone(book)

    def test_field_assignment(self):
        book = self.Book()
        book.title = 'New Title'
        self.assertEqual(book.title, 'New Title')

    def test_to_json(self):
        book = self.Book()
        book.title = 'Foo Bar Book'
        book.rank = 10
        got = book.to_json()
        expected = {
            'id': None,
            'title': 'Foo Bar Book',
            'rank': 10,
        }
        self.assertEqual(got, expected)

    def test_initial_data(self):
        book = self.Book(title='Foo', rank=5)
        self.assertEqual(book.title, 'Foo')
        self.assertEqual(book.rank, 5)


class DefaultFieldValueTest(TestCase):

    def setUp(self):
        class Book(Model):
            title = StringField(default='Untitled Book')

        self.Book = Book

    def test_new_model(self):
        book = self.Book()
        self.assertEqual(book.title, 'Untitled Book')

    def test_to_json(self):
        book = self.Book()
        got = book.to_json()
        expected = {
            'id': None,
            'title': 'Untitled Book',
        }
        self.assertEqual(got, expected)
