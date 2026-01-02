
# Audiobook Maker (Free Stack)

An end-to-end tool to convert books (PDF/EPUB/DOCX/TXT) into cleaned audiobooks (MP3) using **free** tools only.

## Features
- Text extraction with PyMuPDF/pdfminer; **OCR** with Tesseract for scanned PDFs.
- Cleaning heuristics: removes page numbers, repeated headers/footers, fixes ligatures, de-hyphenates line breaks, drops footnote markers, normalizes whitespace.
- Basic **chapter detection** and sentence-aware chunking for natural TTS breaks.
- Two free TTS engines:
  - **gTTS** (Google Text-to-Speech; free online)
  - **pyttsx3** (offline; uses SAPI5/NSSpeech/eSpeak). Quality varies by OS voices.
- MP3 merging with metadata (title/author). Generates per-chapter MP3s + full audiobook MP3.
- Language detection to auto-pick gTTS `lang` (default English).

## Install

1) Python 3.9+
2) System dependencies:
   - **Tesseract OCR** (needed if you use `--ocr` or your PDF is scanned)
   - **ffmpeg** (for MP3 merge/convert)
   - (optional) **eSpeak NG** if you want offline voices on Linux with `pyttsx3`

3) Python deps:
```bash
pip install -r requirements.txt
```

## Usage

### Quick start (normal PDF/EPUB/TXT)
```bash
python audiobook_maker.py --input book.pdf --outdir out --title "My Book" --author "Author Name"
```

### Scanned PDFs (force OCR)
```bash
python audiobook_maker.py --input book_scanned.pdf --ocr --dpi 300 --outdir out
```

### Offline TTS (no internet)
```bash
python audiobook_maker.py --input book.pdf --tts-engine pyttsx3 --outdir out
# Optional: pick a voice (substring match)
python audiobook_maker.py --input book.pdf --tts-engine pyttsx3 --voice "Female" --outdir out
```

### Hindi or other languages (OCR + TTS)
- Install Tesseract language pack (e.g., Hindi `hin`).
- Use `--ocr-lang hin`. Language detection also influences gTTS language.

```bash
python audiobook_maker.py --input book.pdf --ocr --ocr-lang hin --outdir out --title "एक किताब" --author "लेखक"
```

## Tips for Better Cleaning
- If headers/footers remain, open `manifest.json` to see chapter sizes and adjust:
  - Increase threshold in `strip_repeating_headers_footers(text, threshold=15)` if needed.
- If hyphenation persists, raise regex aggressiveness or run pre-clean substitution for common patterns.
- For perfect chapters, rename generated `chapterNNN.mp3` files afterwards.

## Output
- `manifest.json` – chapter manifest
- `chapterNNN.mp3` – one per detected chapter
- `<title>_audiobook.mp3` – full book merged

## Common Issues
- **ffmpeg not found**: install ffmpeg and ensure it's in PATH.
- **Tesseract not found**: install Tesseract and ensure `tesseract` is in PATH.
- **Voices low quality offline**: try gTTS or install better SAPI/eSpeak voices.

## License
MIT
