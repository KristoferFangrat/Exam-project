WITH stage_weather AS (select * from {{ source('EXAM_DB', 'WEATHER_RESOURCE') }})

SELECT DISTINCT
    ID,
    LAT,
    LON,
    TIME,
    TEMPERATURE,
    PRECIPITATION

FROM stage_weather