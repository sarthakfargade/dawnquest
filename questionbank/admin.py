from django.contrib import admin
from .models import Subject, Chapter, Question, QuestionPaper


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject']
    list_filter = ['subject']
    search_fields = ['name']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text_preview', 'chapter', 'q_type', 'difficulty', 'marks']
    list_filter = ['chapter__subject', 'chapter', 'q_type', 'difficulty']
    search_fields = ['text']

    def text_preview(self, obj):
        return obj.text[:60]
    text_preview.short_description = 'Question'


@admin.register(QuestionPaper)
class QuestionPaperAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'total_marks', 'created_at']
    list_filter = ['subject']
