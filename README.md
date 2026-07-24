# TfL BikePoint Investment Dashboard
TfL Data Challenge | Python, SQL, Databricks | Data cleaning, transformation, analysis and interactive dashboard visualisation

Databricks Data Engineering MVP using the TfL BikePoint API to support data-driven BikePoint investment and operational decisions. This version documents the actual MVP that was implemented in Databricks, including the medallion architecture, business framing, business metrics and dashboard outputs.

## Overview
This project was developed as part of a Graduate Data Engineer technical challenge.
The challenge was framed around the Mayor of London exploring potential investment in the TfL BikePoint (Boris Bikes) network. Rather than simply ingesting API data, the objective was to design and implement an end-to-end ETL solution that transforms operational BikePoint data into meaningful business insights.
The solution was built in Databricks using PySpark, SQL, Delta Lake, and a Medallion Architecture (Bronze, Silver, Gold) approach before being surfaced through an interactive dashboard.

The challenge asks for an ETL process using the TfL BikePoint API, with the scenario framed as the Mayor of London considering whether to invest in more Bike Points (“Boris Bikes”). The key requirement is not only to ingest data, but to turn it into something that supports a business conversation. 

This project implements an end-to-end data engineering pipeline using Databricks to analyse the performance of TfL BikePoint stations and support investment-related decision making. The solution follows a medallion architecture approach, ingesting data from the TfL BikePoint API and transforming it into a structured, analytics-ready dataset.

The pipeline includes Bronze, Silver, and Gold layers, handling semi-structured API data and converting it into meaningful business metrics. A Databricks dashboard is used to visualise key insights, including station balance, availability issues, and geographic distribution of demand.
Key focus areas:

- Data pipeline design using Medallion Architecture (Bronze / Silver / Gold)
- Handling and transforming semi-structured JSON data
- Designing clear and actionable business metrics
- Building a dashboard to support data-driven decision making
- Demonstrating scalable and maintainable data engineering practices

## Business Problem

The key business question is:

Are current BikePoint stations balanced, or are there signs of capacity constraints and availability issues that could justify future investment?

The solution focuses on identifying:

- Stations with no bikes available
- Stations with no docking spaces available
- Imbalanced stations with potential capacity issues
- Network-wide availability trends
- Areas that may benefit from operational intervention or future investment

## Architecture
```python
TfL BikePoint API
        │
        ▼
🥉 Bronze Layer
Raw JSON Records
        │
        ▼
🥈 Silver Layer
Parsed & Structured Data
        │
        ▼
🥇 Gold Layer
Business Metrics
        │
        ▼
Databricks Dashboard
```


### Bronze Layer

Stores the API response exactly as received.

Purpose:

- Preserve source data
- Maintain auditability
- Avoid ingestion failures caused by schema changes

Columns:

- json_data
- ingestion_timestamp

### Silver Layer
Transforms semi-structured JSON into an analytical schema.

Key transformations:

- Parse JSON using explicit schema
- Extract station attributes
- Explode nested additionalProperties
- Pivot key-value pairs into columns
- Apply type casting

Core columns:

- station_id
- station_name
- lat
- lon
- nb_bikes
- nb_empty_docks
- nb_docks
- snapshot_timestamp

### Gold Layer

Creates business-facing metrics ready for reporting and dashboards.

#### Metrics

Design principle. The metrics were intentionally kept simple so they would be easy to explain in an interview and easy to surface in a Databricks dashboard. 
Together, these metrics answer the core business questions for the MVP: 

- Occupancy Rate
- Empty Station Flag
- Full Station Flag
- Capacity Stress Score

| Metric          | Logic                       | Business Meaning                |
| --------------- | --------------------------- | ------------------------------- |
| Occupancy Rate  | `nb_bikes / nb_docks`       | Indicates how full a station is |
| Is Empty        | `nb_bikes = 0`              | Users cannot hire a bike        |
| Is Full         | `nb_empty_docks = 0`        | Users cannot return a bike      |
| Capacity Stress | `ABS(0.5 - occupancy_rate)` | Measures station imbalance      |


## Technologies

- Databricks
- PySpark
- SQL
- Delta Lake
- Databricks Dashboards
- REST API

## Data Modelling

- Medallion architecture
- Separation of ingestion, transformation and business logic

## Key Findings

Analysis of the TfL BikePoint network suggests that the overall network is not operating near capacity.

### Finding 1: Network-wide underutilisation

The average occupancy rate is approximately 38%, indicating that, on average, stations have more empty docking points than available bikes.

This suggests that the network as a whole may not currently require significant expansion in capacity.

### Finding 2: Localised imbalance

While overall utilisation appears low, a number of stations exhibit high capacity stress scores.

This indicates that some stations are either close to empty or close to full, which can negatively affect customer experience.

### Finding 3: Operational opportunity

The dashboard suggests that operational redistribution of bikes may provide greater value than immediate infrastructure investment.

Rebalancing bikes between stations could potentially reduce the number of empty and full stations while improving service availability across the network.

### Finding 4: Need for historical analysis

The current analysis is based on a snapshot of BikePoint data.

To support investment decisions with greater confidence, the pipeline should be extended to collect historical snapshots and analyse station behaviour over time.

## Recommendations

Based on the MVP analysis:

1. Prioritise operational bike redistribution before expanding the network.
2. Monitor stations with the highest capacity stress scores.
3. Collect historical snapshots to identify persistent imbalance patterns.
4. Reassess the need for new BikePoint infrastructure once long-term utilisation trends are available.

At the time of analysis, the evidence suggests that improving bike distribution across existing stations may deliver greater benefit than immediately investing in additional BikePoint locations.

## Future Improvements

- Databricks Job orchestration
- Incremental pipeline scheduling
- Historical trend analysis
- Data quality checks
- Weather enrichment
- Transport hub enrichment
- Borough-level demand analysis
- CI/CD deployment pipeline

## Portfolio Value

- ✅ Databricks fundamentals
- ✅ PySpark transformations
- ✅ Spark SQL
- ✅ Delta Lake
- ✅ Medallion Architecture
- ✅ Semi-structured data processing
- ✅ Dashboard design
- ✅ Business-focused data engineering

## Author

Anna Grigoriadi
Data Engineer Apprentice | Microsoft Fabric Data Engineer Associate
Databricks • Azure • SQL • PySpark • Data Engineering
