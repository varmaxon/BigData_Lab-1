
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        segment as value_field,
        count(*) as n_records

    from "warehouse"."main"."fct_revenue"
    group by segment

)

select *
from all_values
where value_field not in (
    'B2B','B2C'
)



  
  
      
    ) dbt_internal_test