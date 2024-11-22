WITH _date AS (SELECT * FROM {{ ref('src_date') }}),
_info AS (SELECT * FROM {{ ref('src_info') }}),
_location AS (SELECT * FROM {{ ref('src_location') }})

SELECT
    
    {{dbt_utils.generate_surrogate_key(['_date.id', '_date.datetime'])}} as date_key,
    {{dbt_utils.generate_surrogate_key(['_info.id', '_info.info_name'])}} as info_key,
    {{dbt_utils.generate_surrogate_key(['_location.id', '_location.location_name'])}} as location_key
FROM
    _date
LEFT JOIN
    _info ON _info.id = _date.id
LEFT JOIN   
    _location ON _info.id = _location.id

ORDER BY datetime DESC
