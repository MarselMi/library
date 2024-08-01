from rest_framework.serializers import ModelSerializer
from mainapp import models


class BookSerializer(ModelSerializer):
    class Meta:
        model = models.Book
        fields = [
            'title', 'author', 'genre'
        ]


class BorrowBookSerializer(ModelSerializer):
    class Meta:
        model = models.BorrowedBook
        fields = '__all__'
