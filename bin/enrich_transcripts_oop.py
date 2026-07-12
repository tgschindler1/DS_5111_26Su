#!/usr/bin/env python3
"""Enrich raw transcript text via LLM, extracting technical terms and book names."""

import sys
import os
import json
import argparse
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

class LLMStrategy(ABC):
    """Interface for a strategy that enriches raw transcript text via an LLM."""

    # pylint: disable=too-few-public-methods

    @abstractmethod
    def enrich(self, video_id: str, raw_text: str) -> str:
        """Must accept video id and raw text string and return response string"""

class GeminiStrategy(LLMStrategy):
    """Enriches transcripts via Gemini; strips timestamps and extracts
	technical terms and books"""

    # pylint: disable=too-few-public-methods


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

    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        if not api_key:
            raise ValueError("Missing GEMINI_API_KEY.")
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def enrich(self, video_id: str, raw_text: str) -> str:
        """Takes video id and raw text strings and returns the raw
	   JSON string response from Gemini"""

        prompt = (
            "You are an elite data engineer. "
            f"Clean this transcript text for video_id '{video_id}'.\n"
            "1. Strip all timestamps and duration codes.\n"
            "2. Extract technical architecture terms and books.\n"
        )


        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=f"{prompt}\n\nTranscript:\n{raw_text}",
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=self.response_schema,
                ),
            )
            return response.text
        except Exception as e:
            raise RuntimeError(
                f"Failed processing video {video_id} during LLM generation: {str(e)}"
            ) from e

class TranscriptEnricher:
    """Drives a LLMStrategy over raw JSON lines from stdin, stream JSON to stdout"""

    # pylint: disable=too-few-public-methods

    def __init__(self, strategy: LLMStrategy):
        self.strategy = strategy

    def run_stream(self):
        """Read identifiers from stdin and emit one enriched response per line to stdout."""
        for line in sys.stdin:
            source_line = line.strip()
            if not source_line:
                continue

            try:
                payload = json.loads(source_line)
                video_id = payload["video_id"]
                raw_text = payload["raw_text"]

            # pylint: disable=broad-exception-caught
            except Exception as e:
                sys.stderr.write(f"ERROR processing incoming JSON payload: {str(e)}")
                sys.stderr.flush()
                continue

            try:
                enriched_json = self.strategy.enrich(video_id, raw_text)
                sys.stdout.write(enriched_json + "\n")
                sys.stdout.flush()

            # pylint: disable=broad-exception-caught
            except Exception as e:
                sys.stderr.write(
	        f"Failed processing video {video_id} during LLM generation: {str(e)}")
                sys.stderr.flush()
                continue

def main(argv=None):
    """Parse CLI arguments, build the selected strategy, and run the engine."""

    parser = argparse.ArgumentParser(description="Transcript Enrichment Node.")
    parser.add_argument(
        "--source",
        choices=["gemini"],
        default="gemini",
        help="Target LLM enrichment strategy (Defaults to gemini).",
    )
    parser.add_argument(
        "--model",
        default="gemini-2.5-flash",
        help="Model name to use for the selected strategy.",
    )

    if argv is None:
        argv = []
    args = parser.parse_args(argv)


    if args.source == "gemini":
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            sys.stderr.write("Missing API Key")
            sys.exit(1)

        selected_strategy = GeminiStrategy(api_key=gemini_api_key, model=args.model)

    else:
        raise ValueError(f"Unsupported source strategy: {args.source}")

    engine = TranscriptEnricher(selected_strategy)
    engine.run_stream()

if __name__ == "__main__":
    main(sys.argv[1:])
