-- CREATE OR REPLACE TABLE DIM_VIDEOS AS was removed and converted to dbt syntax
-- the name of the file itself now represents the name of the table/view
-- the 'table' in the next line carries the table/view directive
{{ config(materialized='table') }}

SELECT
    VIDEO_ID,
    CLEANED_TEXT,
    ARRAY_SIZE(TECH_TERMS_ARRAY) AS TECH_TERM_COUNT,
    ARRAY_SIZE(BOOK_NAMES_ARRAY) AS BOOK_NAME_COUNT,
    ARRAY_SIZE(SPLIT(CLEANED_TEXT, ' ')) AS WORD_COUNT,
    LENGTH(CLEANED_TEXT) AS CHAR_COUNT,
    INSERTED_AT AS PROCESSED_AT
-- the line FROM STG_YOUTUBE_TRANSCRIPTS becomes ...
FROM {{ ref('stg_youtube_transcripts') }}
