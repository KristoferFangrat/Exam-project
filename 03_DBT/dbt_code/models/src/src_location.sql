WITH stage_events AS (select * from {{ source('EXAM_DB', 'EVENT_RESOURCE') }})

SELECT 
    id,
    location__name AS location_name,
    location__gps AS location_gps

FROM stage_events
