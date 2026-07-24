#!/usr/bin/env python3
"""Helper functions for building a YouTube Transcript API client and fetching transcripts."""

import logging

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig


def build_ytt_api(proxy_user, proxy_pass):
    """Return a YouTubeTranscriptApi instance, routed through Webshare if credentials exist."""
    if proxy_user and proxy_pass:
        logging.info(
            "Proxy credentials detected. Routing traffic via Webshare Residential network."
        )
        return YouTubeTranscriptApi(
            proxy_config=WebshareProxyConfig(
                proxy_username=proxy_user,
                proxy_password=proxy_pass,
            )
        )

    logging.warning("No proxy credentials found. Running with direct raw local IP routing.")
    return YouTubeTranscriptApi()


def fetch_transcript_text(ytt_api, video_id):
    """Fetch a video's transcript and stitch it into a single timestamped text string."""
    fetched_transcript = ytt_api.fetch(video_id)
    transcript_list = fetched_transcript.to_raw_data()
    return " ".join(
        f"[{item['start']}] {item['text']}" for item in transcript_list
    )
