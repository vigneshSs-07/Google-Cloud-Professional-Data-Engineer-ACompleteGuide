 SELECT
 PassengerId,
 COUNT(Survived) AS survived_details
 FROM
 `vaulted-journal-420209.demo_dataset_001.demo_table`
 GROUP BY
 PassengerId;



CREATE MATERIALIZED VIEW `vaulted-journal-420209.demo_dataset_001.demo_M_view` AS (
 SELECT
 PassengerId,
 COUNT(Survived) AS survived_details
 FROM
 `vaulted-journal-420209.demo_dataset_001.demo_table`
 GROUP BY
 PassengerId
);



DROP MATERIALIZED VIEW `vaulted-journal-420209.demo_dataset_001.demo_M_view`;