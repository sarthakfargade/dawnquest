from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Chapter(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='chapters')
    name = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.subject.name} - {self.name}"


class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    QTYPE_CHOICES = [
        ('mcq', 'Multiple Choice'),
        ('short', 'Short Answer'),
        ('long', 'Long Answer'),
    ]

    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    q_type = models.CharField(max_length=10, choices=QTYPE_CHOICES, default='short')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    marks = models.PositiveIntegerField(default=1)

    # only used when q_type == 'mcq'; store as {"A": "...", "B": "...", ...}
    options = models.JSONField(null=True, blank=True)
    answer = models.TextField(blank=True)

    # useful once you wire up scraping, so you know where each question came from
    source_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:60]


class QuestionPaper(models.Model):
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    total_marks = models.PositiveIntegerField()
    questions = models.ManyToManyField(Question)
    seed = models.IntegerField(null=True, blank=True, help_text="Used to reproduce this exact paper")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
