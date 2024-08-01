from django.urls import path
from django.contrib.auth.decorators import login_required
from mainapp import views


urlpatterns = [
    # регистрация пользователей / авторизация / выход
    path('sign-up/', views.sign_up, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    # использую login_required, чтоб не было возможности просматривать страницы без авторизации
    path('', login_required(views.reader_index_view, login_url='login'), name='main_page'),
    path('books/', login_required(views.my_books_view, login_url='login'), name='my_books'),
    path('debtors/', login_required(views.librarian_index_view, login_url='login'), name='debtors'),
]
