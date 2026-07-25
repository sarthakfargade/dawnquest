"""
Ingest questions scraped by BeautifulSoup into the database.

Run it with:
    python manage.py ingest_questions

This reads scraper_source/sample_questions.html via
questionbank/scraping/bs_scraper.py, then creates/updates Subject, Chapter,
and Question rows for each item found. Safe to re-run: existing questions
(matched by chapter + exact text) won't be duplicated.
"""
import os
from django.core.management.base import BaseCommand
from django.conf import settings

from questionbank.models import Subject, Chapter, Question
from questionbank.scraping.bs_scraper import scrape_questions_from_html


class Command(BaseCommand):
    help = "Scrape the sample question bank page and load results into the database"

    def handle(self, *args, **options):
        sample_path = os.path.join(settings.BASE_DIR, "scraper_source", "sample_questions.html")

        if not os.path.exists(sample_path):
            self.stderr.write(self.style.ERROR(f"Sample file not found at {sample_path}"))
            return

        self.stdout.write(f"Scraping {sample_path} ...")
        scraped_items = scrape_questions_from_html(sample_path)
        self.stdout.write(f"Found {len(scraped_items)} question(s) in the source page.")

        created_count = 0
        skipped_count = 0

        for item in scraped_items:
            if not item["subject"] or not item["chapter"] or not item["text"]:
                skipped_count += 1
                continue

            subject, _ = Subject.objects.get_or_create(name=item["subject"])
            chapter, _ = Chapter.objects.get_or_create(subject=subject, name=item["chapter"])

            _, created = Question.objects.get_or_create(
                chapter=chapter,
                text=item["text"],
                defaults={
                    "q_type": item.get("q_type", "short"),
                    "difficulty": item.get("difficulty", "medium"),
                    "marks": item.get("marks", 1),
                    "options": item.get("options"),
                    "answer": item.get("answer", ""),
                    "source_url": item.get("source_url", ""),
                },
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done. Added {created_count} new question(s), skipped {skipped_count} invalid item(s)."
        ))