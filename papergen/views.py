from django.shortcuts import render
from questionbank.models import Subject, Chapter
from .services import generate_paper


def generate_paper_view(request):
    subjects = Subject.objects.all()
    result = None

    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        chapter_ids = request.POST.getlist('chapters')
        total_marks = int(request.POST.get('total_marks', 50))

        difficulty_mix = {
            'easy': float(request.POST.get('easy_pct', 30)) / 100,
            'medium': float(request.POST.get('medium_pct', 50)) / 100,
            'hard': float(request.POST.get('hard_pct', 20)) / 100,
        }

        result = generate_paper(
            subject_id=subject_id,
            chapter_ids=chapter_ids,
            difficulty_mix=difficulty_mix,
            total_marks=total_marks,
        )

    chapters_by_subject = Chapter.objects.select_related('subject').all()

    return render(request, 'papergen/generate.html', {
        'subjects': subjects,
        'chapters': chapters_by_subject,
        'result': result,
    })
