from django.contrib import admin
from mainapp import models


@admin.register(models.CustomUser)
class AdminCustomUser(admin.ModelAdmin):
    pass


@admin.register(models.Genre)
class AdminGenre(admin.ModelAdmin):
    pass


@admin.register(models.Book)
class AdminBook(admin.ModelAdmin):
    pass


@admin.register(models.BorrowedBook)
class AdminBorrowedBook(admin.ModelAdmin):
    list_filter = ['return_date']

