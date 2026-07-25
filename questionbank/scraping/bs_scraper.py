"""
BeautifulSoup scraper for the sample question bank page.

This demonstrates the "pulled the question bank using BeautifulSoup" part
of the resume bullet. It reads an HTML page (local file or, with a small
change, a real URL) and turns each .question block into a plain dict that
matches the shape ingest_questions.py expects.

Run it standalone to sanity-check the output before wiring it into Django:
    python questionbank/scraping/bs_scraper.py
"""
import os
from bs4 import BeautifulSoup


def scrape_questions_from_html(source):
    """
    source: either a local file path OR raw HTML string.
    Returns a list of dicts: subject, chapter, text, q_type, difficulty,
    marks, options (or None), answer, source_url.
    """
    if os.path.exists(source):
        with open(source, encoding="utf-8") as f:
            html = f.read()
        source_label = f"file://{os.path.abspath(source)}"
    else:
        html = source
        source_label = ""

    soup = BeautifulSoup(html, "lxml")
    results = []

    for chapter_section in soup.select("section.chapter"):
        subject = chapter_section.get("data-subject", "").strip()
        chapter = chapter_section.get("data-chapter", "").strip()

        for q_div in chapter_section.select("div.question"):
            q_type = q_div.get("data-type", "short")
            difficulty = q_div.get("data-difficulty", "medium")
            marks = int(q_div.get("data-marks", 1))

            text_tag = q_div.select_one("p.q-text")
            text = text_tag.get_text(strip=True) if text_tag else ""

            options = None
            options_ul = q_div.select_one("ul.options")
            if options_ul:
                options = {
                    li.get("data-key", str(i)): li.get_text(strip=True)
                    for i, li in enumerate(options_ul.select("li"))
                }

            answer_tag = q_div.select_one("p.answer")
            answer = answer_tag.get_text(strip=True) if answer_tag else ""

            results.append({
                "subject": subject,
                "chapter": chapter,
                "text": text,
                "q_type": q_type,
                "difficulty": difficulty,
                "marks": marks,
                "options": options,
                "answer": answer,
                "source_url": source_label,
            })

    return results


if __name__ == "__main__":
    # Quick manual test: run this file directly to see what gets extracted
    here = os.path.dirname(os.path.abspath(__file__))
    sample_path = os.path.join(here, "..", "..", "scraper_source", "sample_questions.html")
    questions = scrape_questions_from_html(sample_path)
    print(f"Scraped {len(questions)} questions:\n")
    for q in questions:
        print(f"[{q['subject']} / {q['chapter']}] ({q['difficulty']}, {q['marks']} marks): {q['text']}")