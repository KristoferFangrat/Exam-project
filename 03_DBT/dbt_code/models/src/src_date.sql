WITH stage_events AS (select * from {{ source('EXAM_DB', 'EVENT_RESOURCE') }})

SELECT DISTINCT
    id,
    datetime

from stage_events 
WHERE id IS NOT NULL
AND datetime IS NOT NULL
ORDER BY datetime DESC