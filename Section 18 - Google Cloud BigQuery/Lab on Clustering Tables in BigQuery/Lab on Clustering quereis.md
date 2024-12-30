>>> **PROFESSIONAL DATA ENGINEER** - *Google Cloud Platform*
------------------------

> TITLE: "Introduction to Google Cloud - Clustering Tables in BigQuery"
> 
> Author:
  >- Name: "Vignesh Sekar"
  >- Designation: "Multi Cloud Architect"
  >- Tags: [Google Cloud, DataEngineer, Python, PySpark, SQL, BigData]

-----------------------------------------------------------------------------------------------------------------------

### Clustering based on name, CountryID, Country Column - customer_data.csv

1. SELECT * FROM `lucky-leaf-396003.demo_dataset_003.cluster_demo` LIMIT 100

2. select * from `lucky-leaf-396003.demo_dataset_003.cluster_demo` where Name like 'B%'

3. select * from `lucky-leaf-396003.demo_dataset_003.cluster_demo` where Name like 'B%' and CountryID='MA'

4. select sum(Payment) as payment_boston from `lucky-leaf-396003.demo_dataset_003.cluster_demo` where Name like 'B%' and CountryID='MA' group by Name 


-----------------------------------------------------------------------------------------------------------------------


  <div class="footer">
              copyright © 2022—2023 Cloud & AI Analytics. 
                                      All rights reserved
          </div>