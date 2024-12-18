WITH _date AS (SELECT * FROM {{ ref('src_date') }}),
_info AS (SELECT * FROM {{ ref('src_info') }}),
_location AS (SELECT * FROM {{ ref('src_location') }}),
_weather AS (SELECT * FROM {{ ref('src_weather') }})

SELECT DISTINCT
    {{dbt_utils.generate_surrogate_key(['_date.id', '_date.datetime'])}} as date_key,
    {{dbt_utils.generate_surrogate_key(['_info.id', '_info.info_name'])}} as info_key,
    {{dbt_utils.generate_surrogate_key(['_location.id', '_location.location_name'])}} as location_key,
    {{dbt_utils.generate_surrogate_key(['date_key', 'info_key'])}} as events_key,
    {{dbt_utils.generate_surrogate_key(['_weather.id', '_weather.LAT'])}} as weather_key
    
    
FROM
    _date
LEFT JOIN
    _weather ON _date.id = _weather.id
LEFT JOIN
    _info ON _weather.id = _info.id
LEFT JOIN   
    _location ON _info.id = _location.id

