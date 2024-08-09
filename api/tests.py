from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from mainapp.models import Book, Genre, BorrowedBook, CustomUser
from api.serializers import BookSerializer, BorrowBookSerializer
import logging


class BookAPITestCase(TestCase):

    def setUp(self):
        """Создаем тестовые данные перед каждым тестом."""
        self.client = Client()

        self.user_data = {
            'username': 'test_user',
            'password': 'password123',
            'tab_number': '4568-5654-asd',
            'address': 'Russin Federation, Moskow, Lenina street 24',
            'is_librarian': False
        }
        self.user = CustomUser.objects.create_user(**self.user_data)
        response_token = self.client.post(
            '/api-v1/token/',
            {'username': 'test_user', 'password': 'password123'}
        )
        self.assertEqual(response_token.status_code, status.HTTP_200_OK)
        self.token = response_token.data.get('access')

        self.genre_data = {'name': 'Роман'}
        self.genre = Genre.objects.create(**self.genre_data)
        # logging.log(msg=self.token, level=1)

        self.book_data = {
            'title': 'The Lord of the Rings',
            'author': 'J.R.R. Tolkien',
            'genre': self.genre
        }
        self.book = Book.objects.create(**self.book_data)

    def test_get_book_list(self):
        """Проверяем получение списка книг."""
        response = self.client.get(
            reverse('book'),
            headers={'Authorization': f'Bearer {self.token}'}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BookSerializer(Book.objects.all(), many=True).data, response.data)

    def test_take_book(self):
        """Проверяем взятие книги с библиотеки."""
        response = self.client.post(
            reverse('get_book', args=[self.book.pk]),
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual({'status': 'OK'}, response.data)

    def test_get_borrow_books_list(self):
        """Проверяем получение списка книг."""
        response = self.client.get(
            reverse('borrow_books'),
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BorrowBookSerializer(BorrowedBook.objects.all(), many=True).data, response.data)

    def test_return_book(self):
        """Возврат книги в библиотеку"""
        response = self.client.post(
            reverse('borrow_book', args=[self.book.pk]),
            headers={'Authorization': f'Bearer {self.token}'}
        )
        logging.log(msg=f"test_get_book_list {response.data}", level=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual({'status': 'OK'}, response.data)
