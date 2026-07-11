#!/usr/bin/env python3
"""Enrich raw transcript text via LLM, extracting technical terms and book names."""

from abc import ABC, abstractmethod

class LLMStrategy(ABC):
    """Interface for a strategy that enriches raw transcript text via an LLM."""

    # pylint: disable=too-few-public-methods

    @abstractmethod
    def enrich(self, payload: dict) -> str:
        """Must accept a payload dict and return response string"""
