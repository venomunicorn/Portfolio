
#!/usr/bin/env python3
"""
audiobook_maker.py
------------------
Free, local-first pipeline to convert a book (PDF/EPUB/TXT/DOCX) into a cleaned audiobook (MP3).
- Extracts text (PDF -> text, optional OCR for scanned PDFs)
- Cleans & normalizes (dehyphenate, remove headers/footers/page #s, fix ligatures, collapse whitespace)
- Splits into chapter-ish chunks at sentence boundaries
- Generates audio (free options: gTTS online, or pyttsx3/espeak offline)
- Merges segments into chapter MP3s and a full audiobook MP3; embeds basic metadata.

Requirements (see requirements.txt):
  fitz (PyMuPDF), pdfminer.six (fallback), pdf2image, pytesseract, pillow,
  python-docx, ebooklib, langdetect, pydub, gTTS, pyttsx3 (optional)
Also install system deps:
  - Tesseract OCR (https://tesseract-ocr.github.io/) if you need OCR
  - ffmpeg for MP3 merging (pydub uses it)
  - (optional) eSpeak NG for pyttsx3 offline voices

Usage:
  python audiobook_maker.py --input path/to/book.pdf --outdir ./output --title "My Book" --author "Author"
  # For scanned PDFs that need OCR:
  python audiobook_maker.py --input book_scanned.pdf --ocr --dpi 300
  # Use offline TTS (pyttsx3) instead of gTTS:
  python audiobook_maker.py --input book.pdf --tts-engine pyttsx3
"""

import argparse
import os
import re
import sys
import json
import math
import tempfile
from pathlib import Path
from typing import List, Tuple, Optional

# Optional imports guarded where used
def _optional_import(name):
    try:
        return __import__(name)
    except Exception as e:
        return None

def eprint(*a, **k): 
    print(*a, file=sys.stderr, **k)

# -----------------------------
# File type detection & extract
# -----------------------------

def is_scanned_pdf(pdf_path: Path) -> bool:
    """Heuristic: try to extract any text with PyMuPDF; if very little, assume scanned."""
    fitz = _optional_import("fitz")  # PyMuPDF
    if not fitz:
        return False  # can't tell; caller decides
    try:
        doc = fitz.open(pdf_path)
        text_len = 0
        check_pages = min(5, len(doc))
        for i in range(check_pages):
            text = doc.load_page(i).get_text("text") or ""
            text_len += len(text.strip())
        doc.close()
        return text_len < 200  # likely scanned
    except Exception:
        return False

def extract_text_pdf_pymupdf(pdf_path: Path) -> str:
    fitz = __import__("fitz")
    doc = fitz.open(pdf_path)
    texts = []
    for i in range(len(doc)):
        txt = doc.load_page(i).get_text("text")
        texts.append(txt)
    doc.close()
    return "\n".join(texts)

def extract_text_pdf_pdfminer(pdf_path: Path) -> str:
    from pdfminer.high_level import extract_text
    return extract_text(str(pdf_path))

def ocr_pdf_to_text(pdf_path: Path, dpi: int = 300, lang: str = "eng") -> str:
    """OCR a PDF by rendering pages to images then running Tesseract."""
    from pdf2image import convert_from_path
    import pytesseract
    pages = convert_from_path(str(pdf_path), dpi=dpi)
    texts = []
    for i, img in enumerate(pages, 1):
        eprint(f"OCR: page {i}/{len(pages)}")
        page_text = pytesseract.image_to_string(img, lang=lang)
        texts.append(page_text)
    return "\n".join(texts)

def extract_text_epub(epub_path: Path) -> str:
    from ebooklib import epub
    from bs4 import BeautifulSoup
    book = epub.read_epub(str(epub_path))
    chunks = []
    for item in book.get_items():
        if item.get_type() == 9:  # DOCUMENT
            soup = BeautifulSoup(item.get_content(), "html.parser")
            for s in soup(["script","style"]):
                s.decompose()
            chunks.append(soup.get_text(separator="\n"))
    return "\n".join(chunks)

def extract_text_docx(docx_path: Path) -> str:
    import docx
    d = docx.Document(str(docx_path))
    return "\n".join(p.text for p in d.paragraphs)

def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")

def extract_text(input_path: Path, ocr: bool, dpi: int, ocr_lang: str) -> str:
    ext = input_path.suffix.lower()
    if ext == ".pdf":
        if ocr or is_scanned_pdf(input_path):
            eprint("Using OCR path for PDF...")
            return ocr_pdf_to_text(input_path, dpi=dpi, lang=ocr_lang)
        # try PyMuPDF then pdfminer
        try:
            return extract_text_pdf_pymupdf(input_path)
        except Exception:
            eprint("PyMuPDF failed; falling back to pdfminer.six")
            return extract_text_pdf_pdfminer(input_path)
    elif ext == ".epub":
        return extract_text_epub(input_path)
    elif ext in (".docx", ".doc"):
        return extract_text_docx(input_path if ext==".docx" else Path(convert_doc_to_docx(str(input_path))))
    elif ext in (".txt", ".md"):
        return read_text_file(input_path)
    else:
        raise ValueError(f"Unsupported input type: {ext}")

def convert_doc_to_docx(doc_path: str) -> str:
    """Best-effort .doc -> .docx via libreoffice if available."""
    out = Path(doc_path).with_suffix(".docx")
    if out.exists():
        return str(out)
    try:
        import subprocess, shutil
        if shutil.which("soffice"):
            subprocess.run(["soffice","--headless","--convert-to","docx",doc_path,"--outdir",str(Path(doc_path).parent)], check=True)
            return str(out)
    except Exception:
        pass
    raise RuntimeError(".doc conversion requires LibreOffice 'soffice' in PATH.")

# -----------------------------
# Cleaning & normalization
# -----------------------------

LIGATURES = {
    "ﬁ": "fi",
    "ﬂ": "fl",
    "ﬀ": "ff",
    "ﬃ": "ffi",
    "ﬄ": "ffl",
    "—": "-",
    "–": "-",
    "…": "...",
    "\u00A0": " ",
}

def fix_ligatures(text: str) -> str:
    for k, v in LIGATURES.items():
        text = text.replace(k, v)
    return text

def remove_page_numbers(text: str) -> str:
    # Remove standalone digit lines or lines with only digits + whitespace
    return re.sub(r"(?m)^\s*\d+\s*$", "", text)

def dehyphenate_line_breaks(text: str) -> str:
    # Join words split across lines: e.g., "trans-\nformation" -> "transformation"
    text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)
    return text

def collapse_whitespace(text: str) -> str:
    # Normalize CRLF and multiple blank lines
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    # Max 2 consecutive newlines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def strip_repeating_headers_footers(text: str, min_len=4, threshold=15) -> str:
    """
    Heuristic: remove short lines that repeat many times (likely headers/footers).
    threshold=15 means lines appearing >= 15 times are stripped.
    """
    lines = text.splitlines()
    freq = {}
    for ln in lines:
        s = ln.strip()
        if len(s) >= min_len and len(s) <= 80:
            freq[s] = freq.get(s, 0) + 1
    bad = {s for s,c in freq.items() if c >= threshold}
    if not bad:
        return text
    cleaned = []
    for ln in lines:
        if ln.strip() in bad:
            continue
        cleaned.append(ln)
    return "\n".join(cleaned)

def remove_footnotes_inline(text: str) -> str:
    # Remove bracketed reference markers like [1], [23] mid-sentence
    text = re.sub(r"\s*\[(?:\d{1,3}|[a-z]{1,3})\]", "", text)
    # Remove superscript-like markers: e.g., text^12 -> text (conservative)
    text = re.sub(r"\^\d{1,3}", "", text)
    return text

def smart_sentence_split(text: str) -> List[str]:
    # Simple rule-based sentence split; avoids deps. Splits on . ! ? followed by space and capital/quote
    # Also keep abbreviations intact (e.g., "e.g.", "Mr.", "Dr.") via negative lookbehind for common abbrev.
    abbrev = r"(?:Mr|Ms|Mrs|Dr|Prof|Sr|Jr|vs|e\.g|i\.e|cf|etc|No|Fig|Eq|Ch)"
    pattern = rf"(?<!{abbrev})[\.!?]\s+(?=[\"'(\[]?[A-Z0-9])"
    parts = re.split(pattern, text)
    return [p.strip() for p in parts if p.strip()]

def detect_language(text: str) -> str:
    try:
        from langdetect import detect
        return detect(text)
    except Exception:
        return "en"

def detect_chapters(text: str) -> List[Tuple[str, str]]:
    """
    Very light chapter detection: split on lines that look like headings.
    Returns list of (chapter_title, chapter_text).
    """
    lines = text.splitlines()
    chapters = []
    buf = []
    current_title = "Chapter 1"
    chap_num = 1

    def push(ch_title, ch_text):
        chapters.append((ch_title, ch_text.strip()))

    for ln in lines:
        if re.match(r"^\s*(chapter|section|part)\s+[\w\divxlc]+\.?\s*$", ln.strip(), re.I) or \
           (ln.isupper() and 3 <= len(ln) <= 60):
            # New chapter boundary
            if buf:
                push(current_title, "\n".join(buf))
                chap_num += 1
                buf = []
            current_title = ln.strip().title() or f"Chapter {chap_num}"
        else:
            buf.append(ln)
    if buf:
        push(current_title, "\n".join(buf))
    if not chapters:
        # Fallback: one big chapter
        chapters = [("Chapter 1", text)]
    return chapters

def clean_text_pipeline(raw_text: str) -> str:
    t = raw_text
    t = fix_ligatures(t)
    t = remove_page_numbers(t)
    t = strip_repeating_headers_footers(t)
    t = dehyphenate_line_breaks(t)
    t = remove_footnotes_inline(t)
    t = collapse_whitespace(t)
    return t

# -----------------------------
# Chunking
# -----------------------------

def chunk_sentences(text: str, max_chars: int = 4000) -> List[str]:
    sents = smart_sentence_split(text)
    chunks = []
    buf = ""
    for s in sents:
        if len(buf) + len(s) + 1 <= max_chars:
            buf = (buf + " " + s).strip()
        else:
            if buf:
                chunks.append(buf)
            if len(s) <= max_chars:
                buf = s
            else:
                # Hard split very long sentence
                for i in range(0, len(s), max_chars):
                    chunks.append(s[i:i+max_chars])
                buf = ""
    if buf:
        chunks.append(buf)
    return chunks

# -----------------------------
# TTS engines (free)
# -----------------------------

def tts_gtts(text: str, out_mp3: Path, lang_code: str = "en"):
    from gtts import gTTS
    tts = gTTS(text=text, lang=lang_code, slow=False)
    tts.save(str(out_mp3))

def tts_pyttsx3(text: str, out_mp3: Path, voice: Optional[str] = None, rate: int = 180):
    """
    Offline TTS via pyttsx3 (uses SAPI5 on Windows, NSSpeech on macOS, eSpeak on Linux).
    Audio is first saved as WAV then converted to MP3 via pydub/ffmpeg.
    """
    import pyttsx3
    from pydub import AudioSegment
    tmp_wav = out_mp3.with_suffix(".wav")
    engine = pyttsx3.init()
    if rate:
        engine.setProperty('rate', rate)
    if voice:
        for v in engine.getProperty('voices'):
            if voice.lower() in (v.name or "").lower():
                engine.setProperty('voice', v.id)
                break
    engine.save_to_file(text, str(tmp_wav))
    engine.runAndWait()
    # Convert WAV -> MP3
    audio = AudioSegment.from_wav(str(tmp_wav))
    audio.export(str(out_mp3), format="mp3", bitrate="128k")
    try:
        tmp_wav.unlink()
    except Exception:
        pass

# -----------------------------
# MP3 merging & metadata
# -----------------------------

def merge_mp3s(part_files: List[Path], out_path: Path, title: str, artist: str):
    from pydub import AudioSegment
    total = None
    for p in part_files:
        seg = AudioSegment.from_mp3(str(p))
        if total is None:
            total = seg
        else:
            total += seg
    if total is None:
        raise RuntimeError("No audio parts to merge")
    total.export(str(out_path), format="mp3", bitrate="128k", tags={"title": title, "artist": artist})

# -----------------------------
# Main pipeline
# -----------------------------

def build_audiobook(input_path: Path, outdir: Path, title: str, author: str,
                    force_ocr: bool = False, dpi: int = 300, ocr_lang: str = "eng",
                    tts_engine: str = "gtts", voice: Optional[str] = None,
                    max_chars: int = 4000):
    outdir.mkdir(parents=True, exist_ok=True)
    eprint(f"Extracting text from: {input_path}")
    raw = extract_text(input_path, ocr=force_ocr, dpi=dpi, ocr_lang=ocr_lang)
    eprint("Cleaning text...")
    cleaned = clean_text_pipeline(raw)
    lang_code = detect_language(cleaned[:10000])
    eprint(f"Detected language: {lang_code}")
    eprint("Detecting chapters...")
    chapters = detect_chapters(cleaned)

    manifest = {
        "title": title,
        "author": author,
        "language": lang_code,
        "chapters": [{"title": c[0], "char_len": len(c[1])} for c in chapters]
    }
    (outdir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    chapter_mp3s = []
    for idx, (chap_title, chap_text) in enumerate(chapters, 1):
        eprint(f"TTS Chapter {idx}/{len(chapters)}: {chap_title}")
        parts = chunk_sentences(chap_text, max_chars=max_chars)
        part_files = []
        for j, part in enumerate(parts, 1):
            part_mp3 = outdir / f"chapter{idx:03d}_part{j:03d}.mp3"
            if tts_engine == "gtts":
                tts_gtts(part, part_mp3, lang_code=lang_code)
            elif tts_engine == "pyttsx3":
                tts_pyttsx3(part, part_mp3, voice=voice)
            else:
                raise ValueError("Unsupported TTS engine. Use 'gtts' or 'pyttsx3'.")
            part_files.append(part_mp3)
        # Merge chapter parts
        chap_out = outdir / f"chapter{idx:03d}.mp3"
        merge_mp3s(part_files, chap_out, title=f"{title} - {chap_title}", artist=author)
        chapter_mp3s.append(chap_out)
        # Optionally delete part files to save space
        for pf in part_files:
            try: pf.unlink()
            except Exception: pass

    # Merge full book
    full_out = outdir / f"{slugify(title)}_audiobook.mp3"
    eprint("Merging full audiobook...")
    merge_mp3s(chapter_mp3s, full_out, title=title, artist=author)
    eprint(f"Done. Full audiobook at: {full_out}")
    return full_out

def slugify(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s or "audiobook"

def parse_args():
    p = argparse.ArgumentParser(description="Convert book to cleaned audiobook (free/local).")
    p.add_argument("--input", "-i", required=True, help="Path to PDF/EPUB/DOCX/TXT")
    p.add_argument("--outdir", "-o", default="audiobook_out", help="Output folder")
    p.add_argument("--title", "-t", default="Untitled Book", help="Book title for metadata")
    p.add_argument("--author", "-a", default="Unknown Author", help="Author for metadata")
    p.add_argument("--ocr", action="store_true", help="Force OCR (for scanned PDFs)")
    p.add_argument("--dpi", type=int, default=300, help="OCR render DPI")
    p.add_argument("--ocr-lang", default="eng", help="Tesseract language code (e.g., eng, hin)")
    p.add_argument("--tts-engine", choices=["gtts","pyttsx3"], default="gtts", help="Choose free TTS engine")
    p.add_argument("--voice", default=None, help="Voice name substring for pyttsx3 (optional)")
    p.add_argument("--max-chars", type=int, default=4000, help="Max characters per TTS chunk")
    return p.parse_args()

def main():
    args = parse_args()
    input_path = Path(args.input)
    outdir = Path(args.outdir)
    try:
        build_audiobook(
            input_path=input_path,
            outdir=outdir,
            title=args.title,
            author=args.author,
            force_ocr=args.ocr,
            dpi=args.dpi,
            ocr_lang=args.ocr_lang,
            tts_engine=args.tts_engine,
            voice=args.voice,
            max_chars=args.max_chars,
        )
    except Exception as e:
        eprint("ERROR:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
