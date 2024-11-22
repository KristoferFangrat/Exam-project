WITH events AS (SELECT * FROM {{ ref('fct_events') }}),
date AS (SELECT * FROM {{ ref('dim_date') }}),
info AS (SELECT * FROM {{ ref('dim_info') }}),
location AS (SELECT * FROM {{ ref('dim_location') }})

SELECT 
    info_name,
    info_summary,
    location_name,
    location_gps,
    date.datetime

FROM events
LEFT JOIN info ON events.info_key = info.info_id
LEFT JOIN date ON events.date_key = date.date_id
LEFT JOIN location ON events.location_key = location.location_id
WHERE info_name IS NOT NULL
