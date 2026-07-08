#!/usr/bin/env python3
"""Extract raw YouTube transcripts via stdin video IDs and emit JSON lines to stdout."""

import sys
import os
import json
import logging
from dotenv import load_dotenv
from lib.youtube_client import build_ytt_api, fetch_transcript_text

load_dotenv()

logging.basicConfig(
    filename='pipeline/logs/pipeline_audit.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def main():
    """Read video IDs from stdin, fetch transcripts, and stream JSON output to stdout."""
    logging.info("Pipeline Step 2A (Raw Extraction) started.")

    proxy_user = os.getenv("WEBSHARE_USER")
    proxy_pass = os.getenv("WEBSHARE_PASSWORD")
    ytt_api = build_ytt_api(proxy_user, proxy_pass)

    for line in sys.stdin:
        video_id = line.strip()
        if not video_id:
            continue

        logging.info("Processing transcript extraction for video: %s", video_id)

        try:
            raw_text = fetch_transcript_text(ytt_api, video_id)
            payload = {"video_id": video_id, "raw_text": raw_text}
            sys.stdout.write(json.dumps(payload) + "\n")
            sys.stdout.flush()
        except Exception as e:  # pylint: disable=broad-exception-caught
            logging.error("Failed to fetch YouTube transcript for %s: %s", video_id, str(e))
            continue

    logging.info("Pipeline Step 2A finished.")


if __name__ == '__main__':
    main()
