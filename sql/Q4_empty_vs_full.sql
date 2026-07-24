SELECT 'Empty stations' AS metric, SUM(is_empty) AS value
FROM workspace.bikepoint_db.gold_bikepoints

UNION ALL

SELECT 'Full stations' AS metric, SUM(is_full) AS value
FROM workspace.bikepoint_db.gold_bikepoints;
