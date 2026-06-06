#!/usr/bin/env python3 

import sys
import re
import logging

def main():
    
    logging.basicConfig(filename="pipeline_autid.log", level=logging.INFO)
    
    def is_valid_youtube_id(id_str):
        """
        checks that id is 11 characters long and contains only allowed characters
        """
        pattern = r'^[A-Za-z0-9_-]+$'
        if len(id) == 11 and bool(re.match(pattern, id)) == True:
            print(id)
        else:  logging.error(f"{id} is not a valid ID")

    
    try:
        for line in sys.stdin:
                id = line.strip()
                is_valid_youtube_id(id)
    
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
