#!/usr/bin/env python3
"""Module for validating YouTube IDs from stdin."""
import sys
import re
import logging


def main():
    """Main function to read and validate YouTube IDs."""
    logging.basicConfig(filename="pipeline_audit.log", level=logging.INFO)

    def is_valid_youtube_id(id_str):
        """Check that id is 11 characters long and contains only allowed characters."""
        pattern = r'^[A-Za-z0-9_-]+$'
        if len(id_str) == 11 and re.match(pattern, id_str):
            print(id_str)
        else:
            logging.error("%s is not a valid ID", id_str)

    try:
        for line in sys.stdin:
            id_str = line.strip()
            is_valid_youtube_id(id_str)

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
