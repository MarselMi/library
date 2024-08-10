from datetime import datetime as dt
from django.test import TestCase
from mainapp.models import Book, BorrowedBook, Genre, CustomUser


class BookModelTest(TestCase):

    def test_book_creation(self):
        """Проверяем создание книги."""
        genre: Genre = Genre.objects.create(name='Роман')
        book: Book = Book.objects.create(
            title='The Lord of the Rings',
            author='J.R.R. Tolkien',
            genre=genre
        )
        self.assertIsInstance(book, Book)
        self.assertEqual(book.title, 'The Lord of the Rings')
        self.assertEqual(book.author, 'J.R.R. Tolkien')
        self.assertEqual(book.genre, genre)

    def test_book_str_representation(self):
        '''Проверка строкового представления'''
        genre: Genre = Genre.objects.create(name='Роман')
        """Проверяем строковое представление книги."""
        book: Book = Book(title='The Hobbit', author='J.R.R. Tolkien', genre=genre)
        self.assertEqual(str(book), 'The Hobbit')


class CustomUserTest(TestCase):

    def test_create_reader_user(self):
        '''Проверка создания читателя'''

        new_user: CustomUser = CustomUser.objects.create_user(
            username='test_user',
            first_name='Иван',
            last_name='Иванов',
            password='password',
            address='Россия, г. Мосвка, ул. Ленина, д.4',
        )

        self.assertIsInstance(new_user, CustomUser)
        self.assertEqual(new_user.username, 'test_user')
        self.assertEqual(new_user.first_name, 'Иван')
        self.assertEqual(new_user.last_name, 'Иванов')
        self.assertEqual(new_user.address, 'Россия, г. Мосвка, ул. Ленина, д.4')

    def test_create_librarian_user(self):
        '''Проверка создания библиотекаря'''

        new_user: CustomUser = CustomUser.objects.create_user(
            username='test_user',
            tab_number='asss-2123-asda',
            is_librarian=True,
            password='password',
        )

        self.assertIsInstance(new_user, CustomUser)
        self.assertEqual(new_user.username, 'test_user')
        self.assertEqual(new_user.tab_number, 'asss-2123-asda')
        self.assertEqual(new_user.is_librarian, True)


class ReaderBorrowedBookTest(TestCase):

    def setUp(self):
        '''Создаем основные обьекты для прохождения тестов'''
        genre: Genre = Genre.objects.create(name='Роман')
        self.book: Book = Book.objects.create(
            title='The Lord of the Rings',
            author='J.R.R. Tolkien',
            genre=genre
        )

        self.new_user: CustomUser = CustomUser.objects.create_user(
            username='test_user',
            first_name='Иван',
            last_name='Иванов',
            password='password',
            address='Россия, г. Мосвка, ул. Ленина, д.4',
        )

    def test_take_book(self):
        '''Тест на получение книги читателем'''
        borrowed_book = self.create_borrowed_book(
            book=self.book, new_user=self.new_user
        )

        self.assertIsInstance(borrowed_book, BorrowedBook)
        self.assertIsInstance(borrowed_book.book, Book)
        self.assertEqual(borrowed_book.borrow_date, dt.now().date())
        self.assertEqual(borrowed_book.book, self.book)
        self.assertEqual(borrowed_book.return_date, None)
        self.assertEqual(borrowed_book.reader, self.new_user)

    def test_return_book(self):
        '''Тест на возврат книги в библиотку'''
        borrowed_book = self.create_borrowed_book(
            book=self.book, new_user=self.new_user
        )

        book: Book = Book.objects.filter(pk=self.book.pk)[0]
        book.unavailable_readers.remove(self.new_user)
        return_book: BorrowedBook = BorrowedBook.objects.filter(
            book=book, reader=self.new_user
        )
        return_date = dt.now()
        return_book.update(return_date=return_date)

        self.assertIsInstance(return_book[0], BorrowedBook)
        self.assertIsInstance(return_book[0].book, Book)
        self.assertEqual(return_book[0].return_date, dt.now().date())
        self.assertEqual(borrowed_book.borrow_date, dt.now().date())
        self.assertEqual(borrowed_book.book, self.book)
        self.assertEqual(borrowed_book.reader, self.new_user)

    @staticmethod
    def create_borrowed_book(book: Book, new_user: CustomUser) -> BorrowedBook:
        '''Создание выданной книги читателю'''
        take_book: Book = Book.objects.filter(pk=book.pk)[0]
        take_book.unavailable_readers.add(int(new_user.pk))

        new_borrow_data: dict = {
            'book': take_book,
            'reader': new_user,
        }
        borrowed_book: BorrowedBook = BorrowedBook.objects.create(**new_borrow_data)
        return borrowed_book


class LibrarianTest(TestCase):

    def setUp(self):
        '''Создаем основные обьекты для прохождения тестов'''
        genre: Genre = Genre.objects.create(name='Роман')
        self.book: Book = Book.objects.create(
            title='The Lord of the Rings',
            author='J.R.R. Tolkien',
            genre=genre
        )

        self.reader_user: CustomUser = CustomUser.objects.create_user(
            username='test_user',
            first_name='Иван',
            last_name='Иванов',
            password='password',
            address='Россия, г. Мосвка, ул. Ленина, д.4',
        )

        self.librarian_user: CustomUser = CustomUser.objects.create_user(
            username='librarian',
            is_librarian=True,
            tab_number='123-12-1234',
            password='password',
        )

    def test_show_borrowed_books_by_readers(self):
        '''Показать пользователей у которых хранятся книги взятые с библиотеки'''
        borrowed_book: BorrowedBook = self.create_borrowed_book(
            book=self.book, new_user=self.reader_user
        )
        debtor_books: BorrowedBook = BorrowedBook.objects.filter(return_date=None)

        self.assertIsInstance(borrowed_book, BorrowedBook)
        self.assertIsInstance(debtor_books[0], BorrowedBook)
        self.assertEqual(len(debtor_books), 1)
        self.assertEqual(borrowed_book.reader, self.reader_user)
        self.assertEqual(debtor_books[0].reader, self.reader_user)
        self.assertEqual(debtor_books[0].reader, borrowed_book.reader)
        self.assertEqual(debtor_books[0].book, borrowed_book.book)
        self.assertEqual(debtor_books[0].borrow_date, borrowed_book.borrow_date)
        self.assertEqual(debtor_books[0].return_date, borrowed_book.return_date)

    def test_show_none_debtors_readers(self):
        borrowed: BorrowedBook = self.create_borrowed_book(
            book=self.book, new_user=self.reader_user
        )

        self.return_borrowed_book(reader=self.reader_user, book=self.book, borrowed=borrowed)

        debtor_books: BorrowedBook = BorrowedBook.objects.filter(return_date=None)

        self.assertEqual(len(debtor_books), 0)

    @staticmethod
    def create_borrowed_book(book: Book, new_user: CustomUser) -> BorrowedBook:
        '''Создание выданной книги читателю'''
        take_book: Book = Book.objects.filter(pk=book.pk)[0]
        take_book.unavailable_readers.add(int(new_user.pk))

        new_borrow_data: dict = {
            'book': take_book,
            'reader': new_user,
        }
        borrowed_book: BorrowedBook = BorrowedBook.objects.create(**new_borrow_data)
        return borrowed_book

    @staticmethod
    def return_borrowed_book(reader: CustomUser, book: Book, borrowed: BorrowedBook):
        book: Book = Book.objects.filter(pk=book.pk)[0]
        book.unavailable_readers.remove(reader)
        taked_book: BorrowedBook = BorrowedBook.objects.filter(id=borrowed.pk)
        taked_book.update(return_date=dt.now())
