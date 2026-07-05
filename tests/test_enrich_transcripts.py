#!/usr/bin/env python3 

import sys
import io
import json
import pytest
import os
from bin.enrich_transcripts import main

# 1. Build a dummy container mimicking the Gemini SDK response hierarchy
class MockGeminiResponse:
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
    # 2. Mock out the core GenAI Client methods
    def mock_generate_content(self, model, contents, config=None):
        # Return a pre-baked, schema-compliant JSON string mimicking the model output
        mock_data = {
            "video_id": "ds5111_v001",
            "cleaned_text": "Welcome to class. Today we are testing mock frameworks.",
            "tech_terms": ["mock frameworks"],
            "book_names": []
        }
        return MockGeminiResponse(json.dumps(mock_data))

    # Corrected Module Target: Patch the actual Models service class inside the SDK
    from google.genai.models import Models
    monkeypatch.setattr(Models, "generate_content", mock_generate_content)

    # 3. Simulate your stream input pipeline using an in-memory text buffer
    mock_input_row = {"video_id": "ds5111_v001", "raw_text": "00:01 Welcome to class. Today we are testing mock frameworks."}
    mock_stdin = io.StringIO(json.dumps(mock_input_row) + "\n")
    monkeypatch.setattr(sys, "stdin", mock_stdin)

    # 4. Trigger the main pipeline script execution loop
    main()

    # 5. Intercept the standard console text buffers
    captured = capsys.readouterr()
    stdout_lines = captured.out.strip().split("\n")

    # 6. Execute data integrity validation assertions
    assert len(stdout_lines) == 1
    parsed_output = json.loads(stdout_lines[0])
    assert parsed_output["video_id"] == "ds5111_v001"
    assert "mock frameworks" in parsed_output["tech_terms"]

@pytest.mark.parametrize("video_id,mock_text", [
    ("fake_video_001", "Short single-line transcript text."),
    ("fake_video_002", "A much longer transcript segment with multiple lines included here."),
    ("fake_video_003", ""),
])
def test_extract_transcripts_various_inputs(monkeypatch, capsys, video_id, mock_text):
    class MockTranscriptContainer:
        def to_raw_data(self):
            return [{"start": 0.0, "text": mock_text}]

    def stubbed_fetch_route(self, vid):
        return MockTranscriptContainer()

    monkeypatch.setattr(YouTubeTranscriptApi, "fetch", stubbed_fetch_route)
    monkeypatch.setattr(sys, "stdin", io.StringIO(f"{video_id}\n"))
    main()
    captured = capsys.readouterr()
    stdout_lines = captured.out.strip().split("\n") if captured.out.strip() else []
    if mock_text:
        assert len(stdout_lines) == 1
        parsed = json.loads(stdout_lines[0])
        assert parsed["video_id"] == video_id


@pytest.mark.xfail(reason="enrich_transcripts.py does not yet validate malformed input rows")
def test_enrich_transcripts_malformed_input(monkeypatch, capsys):
    mock_stdin = io.StringIO("not valid json\n")
    monkeypatch.setattr(sys, "stdin", mock_stdin)
    main()
    captured = capsys.readouterr()
    assert captured.out.strip() == ""
