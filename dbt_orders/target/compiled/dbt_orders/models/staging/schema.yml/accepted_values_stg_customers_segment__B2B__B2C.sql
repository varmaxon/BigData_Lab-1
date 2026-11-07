
    
    

with all_values as (

    select
        segment as value_field,
        count(*) as n_records

    from "warehouse"."main"."stg_customers"
    group by segment

)

select *
from all_values
where value_field not in (
    'B2B','B2C'
)


