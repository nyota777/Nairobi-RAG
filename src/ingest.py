# src/ingest.py
import os
from pathlib import Path
from typing import Dict
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
import PyPDF2
from dotenv import load_dotenv

load_dotenv()

BASE = Path(__file__).resolve().parents[1]
DATA_DIR = BASE / "data"
WEB_DIR = DATA_DIR / "web_txt"
PDF_DIR = DATA_DIR / "pdfs"
YT_DIR = DATA_DIR / "yt_transcripts"
WEB_DIR.mkdir(parents=True, exist_ok=True)
PDF_DIR.mkdir(parents=True, exist_ok=True)
YT_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; nairobi-rag/1.0)"}

# Example web sources (add/remove)
WEB_SOURCES: Dict[str, str] = {
    "wikipedia_nairobi.txt": "https://en.wikipedia.org/wiki/Nairobi",
    "nairobi_national_park.txt": "https://en.wikipedia.org/wiki/Nairobi_National_Park",
    "giraffe_centre.txt": "https://en.wikipedia.org/wiki/Giraffe_Centre",
    "nairobi_museum.txt": "https://en.wikipedia.org/wiki/National_Museum_of_Kenya",
    "bomas_of_kenya.txt": "https://en.wikipedia.org/wiki/Bomas_of_Kenya",
    "sheldrick_wildlife_trust.txt": "https://en.wikipedia.org/wiki/Sheldrick_Wildlife_Trust",
    "karura_forest.txt": "https://en.wikipedia.org/wiki/Karura_Forest",
    "nairobi_city.txt": "https://en.wikipedia.org/wiki/Nairobi_City",
    # add blog pages or replace slow sites with reliable mirrors
}

def scrape_page_to_text(url: str) -> str:
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")
    # remove noise
    for tag in soup(["script", "style", "header", "footer", "nav", "noscript"]):
        tag.decompose()
    parts = []
    for el in soup.find_all(["h1","h2","h3","p","li"]):
        txt = el.get_text(separator=" ", strip=True)
        if txt:
            parts.append(txt)
    return "\n\n".join(parts)

def scrape_all_web(save_dir=WEB_DIR):
    for fname, url in WEB_SOURCES.items():
        out = save_dir / fname
        if out.exists() and out.stat().st_size > 1500:
            print(f"Skipping existing {out}")
            continue
        try:
            text = scrape_page_to_text(url)
            out.write_text(text, encoding="utf-8")
            print("Saved", out)
        except Exception as e:
            print("Failed:", url, e)

def extract_text_from_pdf(pdf_path: Path, out_txt: Path):
    # simple extraction - fine for selectable text PDFs
    reader = PyPDF2.PdfReader(str(pdf_path))
    pages = []
    for p in reader.pages:
        text = p.extract_text() or ""
        pages.append(text)
    out_txt.write_text("\n\n".join(pages), encoding="utf-8")
    print("PDF -> text saved", out_txt)

def add_pdf_to_data(pdf_file: str):
    src = Path(pdf_file)
    if not src.exists():
        raise FileNotFoundError(pdf_file)
    outname = src.stem + ".txt"
    out = WEB_DIR / outname
    extract_text_from_pdf(src, out)

def get_youtube_transcript(video_id: str, out_name: str):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = "\n".join([t["text"] for t in transcript])
        out = YT_DIR / f"{out_name}.txt"
        out.write_text(text, encoding="utf-8")
        print("Saved yt transcript ->", out)
    except Exception as e:
        print("YT transcript failed:", video_id, e)

if __name__ == "__main__":
    scrape_all_web()
    # Example: add_pdf_to_data("path/to/your/brochure.pdf")
    # Example: get_youtube_transcript("VIDEO_ID", "video_title")
