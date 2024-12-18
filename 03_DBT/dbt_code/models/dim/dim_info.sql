WITH src_info as (SELECT * FROM {{ ref('src_info') }})

SELECT 
    {{ dbt_utils.generate_surrogate_key(['id', 'info_name'])}} AS info_id,
    info_name,
    info_summary

FROM src_info
WHERE info_name IS NOT NULL
AND info_summary IS NOT NULL