>>> **PROFESSIONAL DATA ENGINEER** - *Google Cloud Platform*
------------------------

> TITLE: "Introduction to Google Cloud - Google Data Catalog"
> 
> Author:
  >- Name: "Vignesh Sekar"
  >- Designation: "Data Engineer"
  >- Tags: [Google Cloud, DataEngineer, Python, PySpark, SQL, BigData]

-----------------------------------------------------------------------------------------------------------------

# Overview

* Data Catalog is a fully managed, scalable metadata management service within Dataplex.
  
* It offers a simple and easy-to-use search interface for data discovery, a flexible and powerful cataloging system for capturing both technical and business metadata, and a strong security and compliance foundation with Cloud Data Loss Prevention (DLP) and Cloud Identity and Access Management (IAM) integrations.

* BigQuery is an enterprise data warehouse that enables super-fast SQL queries using the processing power of Google's infrastructure.

* Simply move your data into BigQuery and let us handle the hard work. You can control access to both the project and your data based on your business needs, such as giving others the ability to view or query your data.


###### Using Data Catalog

* There are two main ways you interact with Data Catalog:
    *  Searching for data assets that you have access to.
    *  Tagging assets with metadata.


### Task 1 - Enable the Data Catalog API

1. From the navigation menu, select APIs and Services > Library.
2. In the search bar, enter in **Data Catalog** and select the first result.
3. Then click Enable.
      1. The Data Catalog API should be successfully enabled.

### Task 2 - Create a dataset

1. In the left navigation pane of BigQuery, click on view actions next to your project id, then click CREATE DATASET.
2. In the Create Dataset dialog:
      1. For Dataset ID, enter demo_dataset
      2. For Data location, select us (multiple regions in United States).
3. Then click Create dataset.


### Task 3 - Copy a public New York Taxi table to your dataset.

1. From the left-hand panel, click + ADD DATA > Public datasets.
2. In the search bar, enter in **NYC TLC Trips** and click on the result that appears:
3. Click out of the side panel to close it as soon as you're ready to continue.
4. Copy the tlc_yellow_trips_2018 table by running this command in your Cloud Shell panel:
      1. bq cp bigquery-public-data:new_york_taxi_trips.tlc_yellow_trips_2018 $(gcloud config get project):demo_dataset.trips
5. Refresh your BigQuery browser page.
6. Confirm that the trips table is listed in your demo_dataset.


### Task 4 - Create a Data Catalog tag template

1. Create a tag template from the Data Catalog UI.
2. Open the Navigation menu and click on Data Catalog > Tag Templates. Then click + CREATE TAG TEMPLATE
3. Fill in the template form to define a "Demo Tag Template".
      1. Template display name: Demo Tag Template
      2. Template ID: demo_tag_template
      3. Location: Region
      4. Next, create four tag attributes (also called tag "fields").
5. Click Add Field. Create four attributes with the values listed below. Note that the "source" attribute defines a required tag attribute. You can use lower case letters and underscores to define attribute names:
      1. **Field display name**: Source of data asset
      2. **Field ID**: source_of_data_asset
      3. **Make this field required**: Checked
      4. **Type**: String
6. Click Done.
7. Now click Add Field and enter in:
      1. **Field display name**:: Number of rows in data asset
      2. **Field ID**: number_of_rows_in_data_asset
      3. **Make this field required**: Not checked
      4. **Type**:  Double
8. Click Done.
9. Then click Add Field and enter in:
      1.  **Field display name**:: Has PII
      2.  **Field ID**: has_pii
      3.  **Make this field required**: Not checked
      4.  **Type**:  Boolean
10. Click Done.
11. Then click Add Field and enter in:
      1. **Field display name**:: PII type
      2. **Field ID**: pii_type
      3. **Make this field required**: Not checked
      4. **Type**:  Enumerated
12. Add 3 values to this attribute:
      1.  Email
      2.  Social Security Number
      3.  None
13. Then click Done.
14. Click CREATE.


### Task 5 - Tag your table with the newly created tags

1. To attach a tag to a table in your dataset, click on the Data Catalog icon in the top left corner.
2. In Left pane, select Search and type demo_dataset in the Search box.
3. Click Search
      1. The demo_dataset and the trips table that you copied into the dataset are displayed in the search results
4. Open the trips table by clicking on the name
5. Click ATTACH TAGS.
6. From the Attach Tags dialog, under "Choose what to tag" select trips table, and select the Demo Tag Template for tag templates.
7. Next, insert or select the following values for each tag attribute:
      1. source_of_data_asset: tlc_yellow_trips_2018
      2. pii_type: NONE
8. Click Save.
9. Click on Demo Tag Template to view the tag attributes listed on the Entry details page.



-----------------------------------------------------------------------------------------------------------------------


  <div class="footer">
              copyright © 2022—2023 Cloud & AI Analytics. 
                                      All rights reserved
          </div>
