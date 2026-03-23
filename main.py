"""
PDF to text converter with optional AI summarization.

Usage:
    uv run main.py <pdf_file> [--summarize] [--verbose]
"""

import argparse
import logging
import os
import sys

from ai_summarizer import summarize_with_openai
from file_utils import derive_output_path, sanitize_filename, write_text_file
from pdf_extractor import extract_pdf_to_text


def _configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        level=level,
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a PDF to text, handling tables and embedded images. "
                    "Optionally summarize the result with OpenAI."
    )
    parser.add_argument("pdf_file", help="Path to the input PDF file")
    parser.add_argument(
        "--summarize",
        action="store_true",
        help="Send extracted text to OpenAI and write an AI-generated summary",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable debug logging",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    _configure_logging(args.verbose)
    logger = logging.getLogger(__name__)

    if not os.path.isfile(args.pdf_file):
        logger.error("File not found: %s", args.pdf_file)
        sys.exit(1)

    # --- Extract PDF to plain text ---
    logger.info("Extracting text from: %s", args.pdf_file)
    text = extract_pdf_to_text(args.pdf_file)

    if not text.strip():
        logger.error("No readable content could be extracted from the PDF")
        sys.exit(1)

    output_path = derive_output_path(args.pdf_file)
    write_text_file(output_path, text)
    print(f"Text saved to: {output_path}")

    # --- Optional AI summarization ---
    if args.summarize:
        logger.info("Requesting AI summary from OpenAI")
        try:
            suggested_name, summary = summarize_with_openai(text)
        except EnvironmentError as exc:
            logger.error("%s", exc)
            sys.exit(1)
        except ValueError as exc:
            logger.error("Summarization failed: %s", exc)
            sys.exit(1)

        summary_path = sanitize_filename(suggested_name, extension=".md")
        write_text_file(summary_path, summary)
        print(f"Summary saved to: {summary_path}")


if __name__ == "__main__":
    main()
