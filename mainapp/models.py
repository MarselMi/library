from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    '''Модель библиотекаря и читателя'''

    tab_number = models.CharField(max_length=10, blank=True, null=True, verbose_name='Табельный номер')
    address = models.TextField(blank=True, null=True, default=None, verbose_name='Адрес проживания')
    is_librarian = models.BooleanField(default=False, verbose_name='Библиотекарь')

    def __str__(self):
        return f'{self.username}'

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователь'
        ordering = ("-pk",)


class Genre(models.Model):
    '''Модель жанра книги'''

    name = models.CharField(max_length=127, blank=True, null=True, verbose_name='Жанр')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Жанры'
        verbose_name_plural = 'Жанр'
        ordering = ("-pk",)


class Book(models.Model):
    '''Модель книги'''

    title = models.CharField(max_length=127, blank=True, null=True, verbose_name='Название')
    author = models.CharField(max_length=255, blank=True, null=True, verbose_name='Автор')
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, verbose_name='Жанр')
    unavailable_readers = models.ManyToManyField('CustomUser')  # Читатели у которых книги на руках

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Книги'
        verbose_name_plural = 'Книга'
        ordering = ("title",)


class BorrowedBook(models.Model):
    """Модель выданной книги"""

    book = models.ForeignKey('Book', on_delete=models.CASCADE, verbose_name='Книга')
    reader = models.ForeignKey('CustomUser', on_delete=models.CASCADE, verbose_name='Читатель')
    borrow_date = models.DateField(auto_now_add=True, verbose_name='Дата получения')
    return_date = models.DateField(default=None, blank=True, null=True, verbose_name='Дата возврата')

    class Meta:
        verbose_name = 'Выданная книга'
        verbose_name_plural = 'Выданные книги'
        ordering = ("book",)

    def __str__(self):
        return f'{self.book}; Читатель: {self.reader}; Дата получения: {self.borrow_date}; Дата возврата: {self.return_date}'
