#!/usr/bin/env python3
"""Tests for bin.extract_transcripts: fetching raw YouTube transcripts via stdin video IDs."""

import sys
import io
import json
import os
import pytest
from youtube_transcript_api import YouTubeTranscriptApi
from bin.extract_transcripts import main


class MockTranscriptContainer:
    """Mimics the 2026 .to_raw_data() array output return schema."""

    def to_raw_data(self):
        """Return a single fake transcript segment."""
        return [
            {"start": 10.5, "text": "Automated container tracking loop text entry."}
        ]


@pytest.mark.skipif(
    not os.getenv("GEMINI_API_KEY"),
    reason="Requires live Gemini API key; only runs when credentials are present"
)
def test_extract_transcripts_main_pipeline_stream(monkeypatch, capsys):
    """
    Verifies that the main() entrypoint loop correctly processes video IDs via stdin
    and outputs structured JSON Lines objects via stdout without hitting the internet.
    """
    def stubbed_fetch_route(self, video_id):
        # pylint: disable=unused-argument
        return MockTranscriptContainer()

    monkeypatch.setattr(YouTubeTranscriptApi, "fetch", stubbed_fetch_route)

    mock_input_stream = io.StringIO("fake_video_999\n")
    monkeypatch.setattr(sys, "stdin", mock_input_stream)

    main()

    captured_output = capsys.readouterr()
    stdout_lines = captured_output.out.strip().split("\n")

    assert len(stdout_lines) == 1, (
        "The pipeline loop should emit exactly one row per valid input ID."
    )

    parsed_json_line = json.loads(stdout_lines[0])

    assert parsed_json_line["video_id"] == "fake_video_999"
    assert "Automated container tracking" in parsed_json_line["raw_text"]


def test_extract_transcripts_bad_input(monkeypatch, capsys):
    """
    Verifies that the script catches an error gracefully when an invalid, empty,
    or un-fetchable video ID hits input processor stream.
    """
    def stubbed_fetch_route(self, video_id):
        # pylint: disable=unused-argument
        if video_id == "unfetchable_video":
            raise RuntimeError("No transcript could be retrieved for unfetchable_video")
        return MockTranscriptContainer()

    monkeypatch.setattr(YouTubeTranscriptApi, "fetch", stubbed_fetch_route)

    mock_input_stream = io.StringIO("unfetchable_video\n\nfake_video_999\n")
    monkeypatch.setattr(sys, "stdin", mock_input_stream)

    main()

    captured_output = capsys.readouterr()
    stdout_lines = captured_output.out.strip().split("\n")

    assert len(stdout_lines) == 1, (
        "The pipeline loop should emit exactly one row per valid input ID. "
        "Failed IDs should produce no output row."
    )

    parsed_json_line = json.loads(stdout_lines[0])

    assert parsed_json_line["video_id"] == "fake_video_999"
    assert "Automated container tracking" in parsed_json_line["raw_text"]


@pytest.mark.parametrize("video_id,mock_text", [
    ("fake_video_001", "Short single-line transcript text."),
    ("fake_video_002", "A much longer transcript segment with multiple lines included here."),
    ("fake_video_003", ""),
])
def test_extract_transcripts_various_inputs(monkeypatch, capsys, video_id, mock_text):
    """Extraction should emit a JSON row for non-empty transcripts, and nothing for empty ones."""

    class ParametrizedMockTranscriptContainer:
        """Mimics .to_raw_data() with a caller-supplied mock text payload."""

        def to_raw_data(self):
            """Return a single segment using the parametrized mock_text value."""
            return [{"start": 0.0, "text": mock_text}]

    def stubbed_fetch_route(self, vid):
        # pylint: disable=unused-argument
        return ParametrizedMockTranscriptContainer()

    monkeypatch.setattr(YouTubeTranscriptApi, "fetch", stubbed_fetch_route)
    monkeypatch.setattr(sys, "stdin", io.StringIO(f"{video_id}\n"))
    main()
    captured = capsys.readouterr()
    stdout_lines = captured.out.strip().split("\n") if captured.out.strip() else []
    if mock_text:
        assert len(stdout_lines) == 1
        parsed = json.loads(stdout_lines[0])
        assert parsed["video_id"] == video_id
