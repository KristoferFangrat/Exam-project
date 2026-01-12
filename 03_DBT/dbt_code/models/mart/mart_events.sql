WITH events AS (SELECT * FROM {{ ref('fct_events') }}),
date AS (SELECT * FROM {{ ref('dim_date') }}),
info AS (SELECT * FROM {{ ref('dim_info') }}),
location AS (SELECT * FROM {{ ref('dim_location') }}),
weather AS (SELECT * FROM {{ ref('dim_weather') }})

SELECT DISTINCT
    info_name AS Event,
    info_summary AS Summary,
    location_name AS Location,
    location_gps AS Coordinates,
    datetime AS Time,
    weather.TEMPERATURE AS Temperature,
    weather.PRECIPITATION AS Precipitation,
    REGEXP_SUBSTR(info_name, ', (.*?),', 1, 1, 'e', 1) AS Category,
    latitude,
    longitude

FROM events
LEFT JOIN info ON events.info_key = info.info_id
LEFT JOIN date ON events.date_key = date.date_id
LEFT JOIN location ON events.location_key = location.location_id
LEFT JOIN weather ON events.weather_key = weather.weather_id
WHERE info_name IS NOT NULL
