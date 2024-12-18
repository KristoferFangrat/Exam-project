WITH src_date as (SELECT * FROM {{ ref('src_date') }})

SELECT DISTINCT
    {{ dbt_utils.generate_surrogate_key(['id', 'datetime']) }} AS date_id,
    TO_TIMESTAMP(datetime) AS datetime

FROM src_date
WHERE datetime IS NOT NULL