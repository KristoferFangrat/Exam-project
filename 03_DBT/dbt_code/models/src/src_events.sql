WITH stage_events AS (select * from {{ source('EXAM_DB', 'EVENT_RESOURCE') }})

SELECT DISTINCT
    event_id,
    location_id,
    info_id,
    date_id,
    weather_id


from stage_events