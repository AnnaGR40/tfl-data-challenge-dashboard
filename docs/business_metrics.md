| Metric          | Logic                       |
| --------------- | --------------------------- |
| Occupancy rate  | `nb_bikes / nb_docks`       |
| Is empty        | `1 when nb_bikes = 0`       |
| Is full         | `1 when nb_empty_docks = 0` |
| Capacity stress | `ABS(0.5 - occupancy_rate)` |
