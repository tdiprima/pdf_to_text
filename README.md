# pdf-to-text

A Python CLI that converts PDF files to plain text, preserving content from tables and embedded images, with an optional AI-powered summary via OpenAI.

## PDFs look clean to humans. Extracting them is a mess.

Research papers and reports are packed with tables, figures, captions, and complex layouts. Basic PDF extractors usually weren’t built to deal with all that. Some ignore images, some turn tables into unreadable chaos, and others just drop chunks of content without telling you. The result? A `.txt` file that seems fine — until you realize half the useful information never made it through.

## Extraction that handles the full page

`pdf-to-text` processes each page through three passes: plain text via `pdfplumber`, table detection rendered as pipe-delimited rows, and OCR on any embedded images via PyMuPDF and Tesseract. Everything is assembled in page order so context is never lost. With `--summarize`, the full extracted text is sent to GPT, which returns the essential points in clear, complete sentences and suggests a descriptive filename — which the tool writes automatically.

## Example

Given `quarterly-report.pdf` with body text, a data table on page 3, and a chart image on page 7:

```
$ uv run main.py quarterly-report.pdf --summarize

Text saved to: quarterly-report.txt
Summary saved to: q3-revenue-highlights-summary.txt
```

`quarterly-report.txt` contains the full extraction, page-by-page, with tables and OCR'd image text inline. `q3-revenue-highlights-summary.txt` contains the AI summary with a filename GPT chose based on the content.

## Usage

**Install dependencies**

```bash
uv sync
```

Tesseract must also be available on your system:

```bash
brew install tesseract
```

**Convert a PDF to text**

```bash
uv run main.py path/to/file.pdf
```

Output is written to the same directory as the input, with `.pdf` replaced by `.txt`.

**Convert and summarize**

```bash
OPENAI_API_KEY=sk-... uv run main.py path/to/file.pdf --summarize
```

Two files are written: the full extraction (same as above) and an AI summary with a GPT-suggested filename, saved in the current working directory.

**Flags**

| Flag | Description |
|---|---|
| `--summarize` | Send extracted text to OpenAI and write a summary |
| `--verbose`, `-v` | Enable debug logging |

<br>
