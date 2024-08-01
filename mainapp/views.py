from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from mainapp import models
from datetime import datetime as dt


def sign_up(request):
    '''Регистрация нового пользователя с выбором роли Читатель либо Библиотекарь'''

    if request.method == 'POST':
        new_user = models.CustomUser

        address = request.POST.get('address')
        tab_number = request.POST.get('tab_number')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')

        new_user.objects.create_user(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
            is_librarian=bool(int(request.POST.get('role'))),
            address=address if address else '',
            tab_number=tab_number if tab_number else None,
            first_name=firstname if firstname else '',
            last_name=lastname if lastname else '',
        )

        # после регистрации перенаправление на страницу авторизации
        return redirect('login')

    data = {'title': 'Регистрация'}

    return render(request, 'register.html', data)


class CustomLoginView(LoginView):
    '''Стандартная авторизация Django-приложения'''
    extra_context = {'title': 'Авторизация'}
    template_name = 'login.html'


class CustomLogoutView(LogoutView):
    '''Стандартный logout Django-приложения'''
    pass


def reader_index_view(request):
    '''Главная страница для Читателя'''

    if request.user.is_librarian:
        # Если пользователь библиотекарь, напрявляю его на страницу с должниками
        return redirect('debtors')

    # Все книги хранящиеся в библиотеке
    all_books = models.Book.objects.all()

    # Книги которые находятся у пользователя
    borrow_books = models.BorrowedBook.objects.filter(reader=request.user, return_date=None)

    if request.method == 'POST':
        if request.POST.get('type') == 'take_book':
            # Обработка AJAX запроса на получение книги
            book_id = request.POST.get('book_id')
            take_book = models.Book.objects.filter(pk=book_id)[0]
            take_book.unavailable_readers.add(int(request.user.id))
            new_borrow_data = {
                'book': take_book,
                'reader': request.user,
            }
            models.BorrowedBook.objects.create(**new_borrow_data)
            return HttpResponse({'status': 'OK'})

        if request.POST.get('type') == 'return_book':
            # Обработка AJAX запроса на возврат книги
            book_id = request.POST.get('book_id')
            book: models.Book = models.Book.objects.filter(pk=book_id)[0]
            book.unavailable_readers.remove(request.user)
            taked_book: models.BorrowedBook = models.BorrowedBook.objects.filter(book=book, reader=request.user)
            taked_book.update(return_date=dt.now())
            return HttpResponse({'status': 'OK'})

    data = {
        'all_books': all_books, 'borrow_books': borrow_books,
    }
    return render(request, 'reader_title.html', data)


def librarian_index_view(request):
    """Гланая страница для Библиотекаря"""

    if request.user.is_librarian is False:
        # Чтоб читатель не мог попасть на страницу Библиотекаря
        return redirect('main_page')

    # выводим книги которые на выдаче
    debtor_books = models.BorrowedBook.objects.filter(return_date=None)
    data = {'debtor_books': debtor_books}
    return render(request, 'librarian_index.html', data)


def my_books_view(request):
    """Страница для просмотр полученных книг и книг которые на руках у читателя"""

    if request.user.is_librarian:
        # Если пользователь библиотекарь, напрявляю его на страницу с должниками
        return redirect('debtors')

    if request.POST.get('type') == 'return_book':
        # Обработка AJAX запроса на возврат книги
        book_id = request.POST.get('book_id')
        borrow_id = request.POST.get('borrow_id')
        book: models.Book = models.Book.objects.filter(pk=book_id)[0]
        book.unavailable_readers.remove(request.user)
        taked_book: models.BorrowedBook = models.BorrowedBook.objects.filter(id=borrow_id)
        taked_book.update(return_date=dt.now())
        return HttpResponse({'status': 'OK'})

    # Вывожу все книги которые получал пользователь
    books_reader = models.BorrowedBook.objects.filter(reader=request.user)

    data = {'books_reader': books_reader}

    return render(request, 'my_books.html', data)

