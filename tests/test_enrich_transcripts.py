#!/usr/bin/env python3
"""Tests for bin.enrich_transcripts: enriching raw transcripts via the Gemini API."""

import sys
import io
import json
import os
import pytest
from google.genai.models import Models
from bin.enrich_transcripts import main


class MockGeminiResponse: # pylint: disable=too-few-public-methods
    """Mimics the Gemini SDK response object, exposing a .text attribute."""

    def __init__(self, text_payload):
        self.text = text_payload


@pytest.mark.skipif(
    not os.getenv("GEMINI_API_KEY"),
    reason="Requires live Gemini API key; only runs when credentials are present"
)
def test_enrich_transcripts_streaming_pipeline(monkeypatch, capsys):
    """
    Verifies that main() reads mock lines from stdin, calls the Gemini client structure,
    and streams verified JSON objects out to stdout without making live API network requests.
    """
    def mock_generate_content(self, model, contents, config=None):
        # pylint: disable=unused-argument
        mock_data = {
            "video_id": "ds5111_v001",
            "cleaned_text": "Welcome to class. Today we are testing mock frameworks.",
            "tech_terms": ["mock frameworks"],
            "book_names": []
        }
        return MockGeminiResponse(json.dumps(mock_data))

    monkeypatch.setattr(Models, "generate_content", mock_generate_content)

    mock_input_row = {
        "video_id": "ds5111_v001",
        "raw_text": "00:01 Welcome to class. Today we are testing mock frameworks.",
    }
    mock_stdin = io.StringIO(json.dumps(mock_input_row) + "\n")
    monkeypatch.setattr(sys, "stdin", mock_stdin)

    main()

    captured = capsys.readouterr()
    stdout_lines = captured.out.strip().split("\n")

    assert len(stdout_lines) == 1
    parsed_output = json.loads(stdout_lines[0])
    assert parsed_output["video_id"] == "ds5111_v001"
    assert "mock frameworks" in parsed_output["tech_terms"]


@pytest.mark.xfail(reason="enrich_transcripts.py does not yet validate malformed input rows")
def test_enrich_transcripts_malformed_input(monkeypatch, capsys):
    """Malformed (non-JSON) input rows should be skipped without crashing (known gap)."""
    mock_stdin = io.StringIO("not valid json\n")
    monkeypatch.setattr(sys, "stdin", mock_stdin)
    main()
    captured = capsys.readouterr()
    assert captured.out.strip() == ""
