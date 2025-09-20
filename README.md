# University Accountability Ordinance Project

## Project Description

Boston's University Accountability Ordinance (UAO) requires institutions to report data relevant to off‑campus student housing. The project will assemble, standardize, and analyze the past decade of student‑housing‑related data (enrollment by address, inspections/violations, 311 complaints, property assessment, and geospatial context) to quantify student presence in rental markets, characterize housing conditions, and surface non‑compliance patterns.

## Goals

The project will compute the share of rental units occupied by students and the trend over time, characterize off‑campus housing conditions for student‑linked addresses, summarize the spectrum and severity of violations identify, non‑compliant landlords and spatial clusters, and track assessed property values (and/or rent proxies) for student‑linked parcels.

## Data Collection

Acquisition of Data: Use official application programming interfaces (APIs) where provided; otherwise acquire datasets via documented bulk download endpoints.

Primary sources are:
- [Building and Property Violations](https://data.boston.gov/dataset/building-and-property-violations1/resource/800a2663-1d6a-46e7-9356-bedb70f5332c)
- [311 Service Request](https://data.boston.gov/dataset/311-service-requests)
- [SAM Addresses](https://data.boston.gov/dataset/live-street-address-management-sam-addresses)
- [Property Assessment Data](https://data.boston.gov/dataset/property-assessment)
- [Student Housing Data (2016 - 2024)](https://docs.google.com/spreadsheets/d/11X4VvywkSodvvTk5kkQH7gtNPGovCgBq/edit?usp=drive_link&ouid=107346197263951251461&rtpof=true&sd=true)
- [Shape files for neighborhoods](https://data.boston.gov/dataset/boston-neighborhood-boundaries-approximated-by-2020-census-tracts)

## Modeling Data

The project will begin with descriptive analysis to understand coverage, quality, and trends, computing clear indicators (e.g., student share of rental units, violation rates, and severity summaries) at the district and property levels. If time allows, the project will have a lightweight predictive component that estimates next‑period non‑compliance risk.

## Visualization of Data

Most important visualizations will be about:
- Student Share by District Over Time 
- Violations Affecting Student Addresses 
- Bad Landlords Overview 
- Problem‑Property Map 
- 311 Complaints vs. Violations 
- Property Values vs. Student Presence 
- Hotspot Clusters using DBSCAN map overlay.

In the case of how to visualize these, it is to be determined.

## Test Plan

If modeling, withhold 20% of time‑sliced data (e.g., last year per district) for out‑of‑sample checks and use time-aware splits (e.g., Train: 2016–2021, Val: 2022, Test: 2023–2024).
