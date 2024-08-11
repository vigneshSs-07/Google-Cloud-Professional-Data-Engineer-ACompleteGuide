 SELECT
 PassengerId,
 COUNT(Survived) AS survived_details
 FROM
 `vaulted-journal-420209.demo_dataset_001.demo_table`
 GROUP BY
 PassengerId;



CREATE VIEW `vaulted-journal-420209.demo_dataset_001.demo_view` AS (
 SELECT
 PassengerId,
 COUNT(Survived) AS survived_details
 FROM
 `vaulted-journal-420209.demo_dataset_001.demo_table`
 GROUP BY
 PassengerId
);



DROP VIEW `vaulted-journal-420209.demo_dataset_001.demo_view`;