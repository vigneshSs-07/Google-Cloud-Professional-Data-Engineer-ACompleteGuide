>>> **PROFESSIONAL DATA ENGINEER** - *Google Cloud Platform*
------------------------

> TITLE: "Introduction to Google Cloud - Partitioned Tables in BigQuery"
> 
> Author:
  >- Name: "Vignesh Sekar"
  >- Designation: "Multi Cloud Architect"
  >- Tags: [Google Cloud, DataEngineer, Python, PySpark, SQL, BigData]

-----------------------------------------------------------------------------------------------------------------------

### Partition based on Ingestion time - invoice_data.csv


1. SELECT * FROM `lucky-leaf-396003.demo_dataset_003.ingestion_parition_demo` WHERE TIMESTAMP_TRUNC(_PARTITIONTIME, DAY) = TIMESTAMP("2023-12-23") LIMIT 10

###### Legacy SQL Dialect

2. select _PARTITIONTIME as pt, _PARTITIONDATE as pd, Name from `lucky-leaf-396003.demo_dataset_003.ingestion_parition_demo` where _PARTITIONDATE = DATE("2023-12-23")

3. select * from [demo_dataset_003.ingestion_parition_demo$__PARTITIONS_SUMMARY__]


### Partition based on TimeStamp Column - nyc_tlc_yellow_trips_2018_subset_1.csv

1. SELECT * FROM `lucky-leaf-396003.kf_demo_dataset_010.timestamp_demo` WHERE TIMESTAMP_TRUNC(pickup_datetime, DAY) = TIMESTAMP("2023-12-25") LIMIT 10

###### Legacy SQL Dialect

2. select * from [kf_demo_dataset_010.timestamp_demo$__PARTITIONS_SUMMARY__]

3. select * from [kf_demo_dataset_010.timestamp_demo$__NULL__]

4. select * from [kf_demo_dataset_010.timestamp_demo$__UNPARTITIONED__]


### Partition based on Integer Column - employee_transcations.csv

1. SELECT * FROM `lucky-leaf-396003.demo_dataset_003.integer_table` where emp_id between 50 and 90

###### Legacy SQL Dialect

2. select * from [demo_dataset_003.integer_table$__UNPARTITIONED__]

3. select * from [demo_dataset_003.integer_table$__NULL__]

4. select * from [demo_dataset_003.integer_table$__PARTITIONS_SUMMARY__]


-----------------------------------------------------------------------------------------------------------------------


  <div class="footer">
              copyright © 2022—2023 Cloud & AI Analytics. 
                                      All rights reserved
          </div>