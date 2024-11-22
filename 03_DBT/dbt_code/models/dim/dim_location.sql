WITH src_location as (SELECT * FROM {{ ref('src_location') }})

SELECT 
    {{ dbt_utils.generate_surrogate_key(['id', 'location_name'])}} AS location_id,
    location_name,
    location_gps

FROM src_location
WHERE location_name IS NOT NULL
AND location_gps IS NOT NULL