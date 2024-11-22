WITH src_date as (SELECT * FROM {{ ref('src_date') }})

SELECT 
    {{ dbt_utils.generate_surrogate_key(['id', 'datetime'])}} AS date_id,
    datetime

FROM src_date
WHERE datetime IS NOT NULL