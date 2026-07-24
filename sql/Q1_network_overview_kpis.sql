USE CATALOG workspace;
USE SCHEMA bikepoint_db;

SELECT
    COUNT(*) AS total_stations,
    ROUND(AVG(occupancy_rate), 3) AS avg_occupancy_rate,
    SUM(is_empty) AS empty_stations,
    SUM(is_full) AS full_stations,
    ROUND(AVG(capacity_stress), 3) AS avg_capacity_stress
FROM gold_bikepoints;
