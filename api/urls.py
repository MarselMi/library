from django.urls import path, include
from api import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# router.register(r'book', views.BookModelView, basename='book')
# router.register(r'borrow_books', views.BorrowBookModelView, basename='borrow_books')


urlpatterns = [
    path('', include(router.urls)),

    # эндпоинты для аутентификации по JWT-token
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', views.MyTokenRefreshView.as_view(), name='token_refresh'),

    # эндпоинты для получения списка книг, и взять книгу для чтения
    path('book/', views.get_list_books, name='book'),
    path('book/<book_id>/', views.get_book_to_read, name='get_books'),

    # эндпоинты для получения списка книг на руках
    path('borrow_books/', views.get_list_borrow_books, name='borrow_books'),
    path('borrow_books/<book_id>/', views.return_book, name='borrow_books'),
]
