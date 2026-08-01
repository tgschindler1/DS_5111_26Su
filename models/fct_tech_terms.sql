-- CREATE OR REPLACE TABLE FCT_TECH_TERMS AS was removed and converted to dbt syntax
-- the name of the file itself now represents the name of the table/view
-- the 'table' in the next line carries the table/view directive
{{ config(materialized='table') }}

SELECT
    VIDEO_ID,
    f.value::STRING AS TECH_TERM,
    INSERTED_AT AS PROCESSED_AT
-- the line FROM STG_YOUTUBE_TRANSCRIPTS becomes ...
FROM {{ ref('stg_youtube_transcripts') }},
LATERAL FLATTEN(input => TECH_TERMS_ARRAY) f
