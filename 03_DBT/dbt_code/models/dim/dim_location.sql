WITH src_location as (SELECT * FROM {{ ref('src_location') }})

SELECT DISTINCT
    {{ dbt_utils.generate_surrogate_key(['id', 'location_name'])}} AS location_id,
    id,
    location_name,
    location_gps,
    SPLIT(location_gps, ',')[0]::FLOAT AS latitude,
    SPLIT(location_gps, ',')[1]::FLOAT AS longitude

FROM src_location
WHERE location_name IS NOT NULL
AND location_gps IS NOT NULL