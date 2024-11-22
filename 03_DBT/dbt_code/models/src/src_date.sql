WITH stage_events AS (select * from {{ source('EXAM_DB', 'EVENT_RESOURCE') }})

SELECT 
    id,
    datetime

from stage_events ORDER BY datetime DESC