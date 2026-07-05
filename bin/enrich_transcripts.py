#!/usr/bin/env python3
"""Enrich raw transcript text via Gemini, extracting technical terms and book names."""

import sys
import os
import json
import logging
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

logging.basicConfig(
    filename='logs/pipeline_audit.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def main():
    """Read raw transcript JSON lines from stdin, enrich via Gemini, stream JSON to stdout."""
    logging.info("Pipeline Step 2B (Gemini Enrichment) started.")

    gemini_api_key = os.getenv("GEMINI_API_KEY")

    if not gemini_api_key:
        logging.critical("Missing GEMINI_API_KEY.")
        sys.exit(1)

    client = genai.Client(api_key=gemini_api_key)

    response_schema = {
        "type": "OBJECT",
        "properties": {
            "video_id": {
                "type": "STRING"
            },
            "cleaned_text": {
                "type": "STRING"
            },
            "tech_terms": {
                "type": "ARRAY",
                "items": {
                    "type": "STRING"
                }
            },
            "book_names": {
                "type": "ARRAY",
                "items": {
                    "type": "STRING"
                }
            }
        },
        "required": [
            "video_id",
            "cleaned_text"
        ]
    }

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            payload = json.loads(line)
            video_id = payload["video_id"]
            raw_text = payload["raw_text"]
        except Exception as e:  # pylint: disable=broad-exception-caught
            logging.error("Failed to parse incoming JSON payload row: %s", str(e))
            continue

        logging.info("Orchestrating Gemini enrichment for video: %s", video_id)

        prompt = f"""
        You are an elite data engineer. Clean this transcript text for video_id '{video_id}'.
        1. Strip all timestamps and duration codes.
        2. Extract technical architecture terms and books.
        """

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"{prompt}\n\nTranscript:\n{raw_text}",
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=response_schema
                )
            )

            sys.stdout.write(response.text + "\n")
            sys.stdout.flush()

        except Exception as e:  # pylint: disable=broad-exception-caught
            logging.error("Failed processing video %s during LLM generation: %s", video_id, str(e))

    logging.info("Pipeline Step 2B finished.")


if __name__ == '__main__':
    main()
