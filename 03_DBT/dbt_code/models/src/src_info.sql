WITH stage_events AS (select * from {{ source('EXAM_DB', 'EVENT_RESOURCE') }})

SELECT 
    id,
    name AS info_name,
    summary AS info_summary

from stage_events