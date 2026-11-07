
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select segment
from "warehouse"."main"."fct_revenue"
where segment is null



  
  
      
    ) dbt_internal_test