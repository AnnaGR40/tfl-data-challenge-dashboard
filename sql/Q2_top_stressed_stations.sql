SELECT
    station_name,
    nb_bikes,
    nb_empty_docks,
    nb_docks,
    ROUND(occupancy_rate, 3) AS occupancy_rate,
    ROUND(capacity_stress, 3) AS capacity_stress
FROM workspace.bikepoint_db.gold_bikepoints
ORDER BY capacity_stress DESC
LIMIT 10;
