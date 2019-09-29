from django.contrib import admin

from .models import Answer


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    search_fields = ['text', ]
    list_display = ['__str__', 'parent', ]
