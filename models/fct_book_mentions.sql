-- CREATE OR REPLACE TABLE FCT_BOOK_MENTIONS AS was removed and converted to dbt syntax
-- the name of the file itself now represents the name of the table/view
-- the 'table' in the next line carries the table/view directive
{{ config(materialized='table') }}

SELECT
    VIDEO_ID,
    f.value::STRING AS BOOK_NAME,
    INSERTED_AT AS PROCESSED_AT
-- the line FROM STG_YOUTUBE_TRANSCRIPTS becomes ...
FROM {{ ref('stg_youtube_transcripts') }},
LATERAL FLATTEN(input => BOOK_NAMES_ARRAY) f

