WITH src_weather as (SELECT * FROM {{ ref('src_weather') }})

SELECT 
    {{ dbt_utils.generate_surrogate_key(['ID','LAT' ])}} AS weather_id,
    ID,
    LAT,
    LON,
    TIME,
    TEMPERATURE,
    PRECIPITATION

FROM src_weather
