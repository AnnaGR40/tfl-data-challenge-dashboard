# tfl-data-challenge-dashboard
TfL Data Challenge | Python, SQL, Databricks | Data cleaning, transformation, analysis and interactive dashboard visualisation

## Context

The challenge asks for an ETL process using the TfL BikePoint API, with the scenario framed as the Mayor of London considering whether to invest in more Bike Points (“Boris Bikes”). The key requirement is not only to ingest data, but to turn it into something that supports a business conversation. 

This project implements an end-to-end data engineering pipeline using Databricks to analyse the performance of TfL BikePoint stations and support investment-related decision making. The solution follows a medallion architecture approach, ingesting data from the TfL BikePoint API and transforming it into a structured, analytics-ready dataset.

The pipeline includes Bronze, Silver, and Gold layers, handling semi-structured API data and converting it into meaningful business metrics. A Databricks dashboard is used to visualise key insights, including station balance, availability issues, and geographic distribution of demand.
Key focus areas:

- Data pipeline design using Medallion Architecture (Bronze / Silver / Gold)
- Handling and transforming semi-structured JSON data
- Designing clear and actionable business metrics
- Building a dashboard to support data-driven decision making
- Demonstrating scalable and maintainable data engineering practices

## Purpose
This version documents the actual MVP that was implemented in Databricks, including the medallion architecture, business framing, business metrics and dashboard outputs. The structure is designed so screenshots can be dropped into the document cleanly. 


# TfL BikePoint Investment Dashboard

## Overview

Databricks-based ETL pipeline and dashboard solution analysing London's BikePoint network to support investment decisions.

## Architecture

Bronze → Silver → Gold Medallion Architecture

## Technologies

- Databricks
- PySpark
- SQL
- Delta Lake
- Databricks Dashboards
- REST API

## Key Metrics

- Occupancy Rate
- Empty Station Flag
- Full Station Flag
- Capacity Stress

Design principle. The metrics were intentionally kept simple so they would be easy to explain in an interview and easy to surface in a Databricks dashboard. 
Metric

Logic
Business meaning
Occupancy rate
nb_bikes / nb_docks
How full a station is. Near 0 means very few bikes; near 1 means very few empty docks.
Is empty
1 when nb_bikes = 0
Users cannot hire a bike from that station.
Is full
1 when nb_empty_docks = 0
Users cannot return a bike to that station.
Capacity stress
ABS(0.5 - occupancy_rate)
Simple imbalance score. Higher values indicate stations farther from a balanced midpoint.


### Why these four metrics

Together, these metrics answer the core business questions for the MVP: 

station balance, user availability issues, and which stations should be prioritised for further investigation. 



## Key Findings

(summary)

## Future Improvements



## Author

Anna Grigoriadi
