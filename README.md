# DawnQuest

Django app for a learning center to dynamically generate randomized question papers
from a structured question bank, populated via web scraping (BeautifulSoup / Scrapy).

## Setup

1. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Create an admin user:
   ```
   python manage.py createsuperuser
   ```

5. Run the dev server:
   ```
   python manage.py runserver
   ```

6. Visit:
   - `http://127.0.0.1:8000/admin` — add Subjects, Chapters, Questions
   - `http://127.0.0.1:8000/` — generate a randomized paper

## Project structure

- `questionbank/` — data models (Subject, Chapter, Question, QuestionPaper) and admin registration
- `papergen/` — the randomized paper generation logic (`services.py`) and the form/view that uses it
- `questionbank/management/commands/ingest_questions.py` — placeholder command where scraped
  data gets loaded into the database once the scraping pipeline is built

## Roadmap

- [ ] Add ~20 sample questions manually via `/admin` to test generation
- [ ] Write a BeautifulSoup scraper for one source, print results to console
- [ ] Write a Scrapy spider, wire its output into `ingest_questions`
- [ ] Add PDF export of generated papers (WeasyPrint)
- [ ] Add instructor authentication
- [ ] Deploy (Render / Railway)
