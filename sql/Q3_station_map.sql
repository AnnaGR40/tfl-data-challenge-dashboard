SELECT
    station_name,
    lat,
    lon,
    ROUND(occupancy_rate, 3) AS occupancy_rate,
    ROUND(capacity_stress, 3) AS capacity_stress
FROM workspace.bikepoint_db.gold_bikepoints;
