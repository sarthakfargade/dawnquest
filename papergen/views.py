from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa

from questionbank.models import Subject, Chapter
from .services import generate_paper


@login_required
def generate_paper_view(request):
    subjects = Subject.objects.all()
    result = None
    chapter_ids = []
    total_marks = 50

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
        'chapter_ids': chapter_ids,
        'total_marks': total_marks,
    })


@login_required
def download_paper_pdf(request):
    """
    Re-generates the exact same paper using the seed carried over in the
    hidden form fields, then renders it to a downloadable PDF.
    """
    subject_id = request.POST.get('subject')
    chapter_ids = request.POST.getlist('chapters')
    total_marks = int(request.POST.get('total_marks', 50))
    seed = request.POST.get('seed')
    seed = int(seed) if seed else None

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
        seed=seed,
    )

    subject = Subject.objects.filter(id=subject_id).first()
    html = render_to_string('papergen/pdf_template.html', {
        'result': result,
        'subject': subject,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="question_paper.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response