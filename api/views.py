from datetime import datetime as dt
from rest_framework import viewsets
from rest_framework.response import Response
from api.serializers import BookSerializer, BorrowBookSerializer
from mainapp.models import Book, BorrowedBook
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)


class MyTokenRefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # доступ только авторизованным пользователям
def get_list_books(request):
    queryset: Book = Book.objects.all()
    serializer = BookSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_book_to_read(request, book_id):

    take_book: Book = Book.objects.filter(pk=book_id)[0]
    take_book.unavailable_readers.add(int(request.user.id))
    new_borrow_data = {
        'book': take_book,
        'reader': request.user,
    }
    BorrowedBook.objects.create(**new_borrow_data)

    return Response({"status": "OK"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_list_borrow_books(request):
    queryset: BorrowedBook = BorrowedBook.objects.filter(reader=request.user.id, return_date=None)
    serializer = BorrowBookSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def return_book(request, book_id):
    book_id = book_id
    book: Book = Book.objects.filter(pk=book_id)[0]
    book.unavailable_readers.remove(request.user)
    taked_book: BorrowedBook = BorrowedBook.objects.filter(book=book_id, reader=request.user.id)
    taked_book.update(return_date=dt.now())
    return Response({"status": "OK"})
