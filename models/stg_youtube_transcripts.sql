-- CREATE OR REPLACE VIEW STG_YOUTUBE_TRANSCRIPTS AS was removed and converted to dbt syntax
-- the name of the file itself now represents the name of the table/view
-- the 'view' in the next line carries the table/view directive
{{ config(materialized='view') }}

SELECT
    JSON_PAYLOAD:video_id::STRING AS VIDEO_ID,
    JSON_PAYLOAD:cleaned_text::STRING AS CLEANED_TEXT,
    JSON_PAYLOAD:tech_terms AS TECH_TERMS_ARRAY,
    JSON_PAYLOAD:book_names AS BOOK_NAMES_ARRAY,
    INSERTED_AT
-- raw_transcripts is our lowest-level raw source table, so it stays a plain FROM clause
FROM JZT6RV.RAW_TRANSCRIPTS
