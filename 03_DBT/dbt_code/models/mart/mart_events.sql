WITH events AS (SELECT * FROM {{ ref('fct_events') }}),
date AS (SELECT * FROM {{ ref('dim_date') }}),
info AS (SELECT * FROM {{ ref('dim_info') }}),
location AS (SELECT * FROM {{ ref('dim_location') }}),
weather AS (SELECT * FROM {{ ref('dim_weather') }})

SELECT DISTINCT
    {{ dbt_utils.generate_surrogate_key(['info_name', 'info_summary']) }} AS mart_id,
    info_name,
    info_summary,
    location_name,
    location_gps,
    datetime,
    weather.TEMPERATURE,
    weather.PRECIPITATION,
    REGEXP_SUBSTR(info_name, ', (.*?),', 1, 1, 'e', 1) AS category

FROM events
LEFT JOIN info ON events.info_key = info.info_id
LEFT JOIN date ON events.date_key = date.date_id
LEFT JOIN location ON events.location_key = location.location_id
LEFT JOIN weather ON events.weather_key = weather.weather_id
WHERE info_name IS NOT NULL
