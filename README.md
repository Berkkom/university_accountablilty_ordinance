# University Accountability Ordinance Project

## Project Description

Boston’s University Accountability Ordinance (UAO) requires local universities to annually report data on off-campus student housing. This project will consolidate, standardize, and analyze a decade’s worth of student-housing-related datasets (2016–2024) to assess student impact on the rental market and identify compliance issues among landlords and properties.

Rather than examining every possible factor, the project focuses on three specific dimensions of accountability:

- Student Occupancy Patterns — measuring where and how student populations are distributed across Boston’s neighborhoods and rental units.
- Housing Condition and Safety — identifying code violations and complaint types that most frequently affect student-linked properties.
- Landlord Compliance Behavior — detecting landlords with repeated or severe violations relative to city averages.

## Goals

The project’s refined objectives are:

### Quantify Student Rental Presence
- Compute the annual share of rental units occupied by students for each Boston neighborhood (2016–2024).
- Success Metric: Accurate student share computed for ≥95% of properties linked to known student addresses.

### Characterize Housing Conditions
- Categorize violations and 311 complaints associated with student-linked properties, focusing on:
  - Sanitation issues (e.g., pest control, waste disposal),
  - Safety hazards (e.g., missing smoke detectors, structural damage),
  - Over-occupancy or unpermitted conversions.
- Success Metric: Generate violation rate distributions per 1,000 student-linked properties and identify top 5 violation types per district.

### Identify Non-Compliant Landlords
- Define “non-compliance” as ≥3 violations within a two-year window or ≥2 severe (safety-related) violations.
- Flag repeat offenders and map clusters of non-compliance using DBSCAN.
- Success Metric: Correctly identify ≥90% of landlords appearing in the city’s public enforcement records for 2023–2024.

If time permits, an exploratory predictive model will estimate the probability of non-compliance in the next reporting period based on violation history and property attributes.

## Data Collection

Sources and Access Methods:

- Building and Property Violations — City of Boston Inspectional Services API
- 311 Service Requests — Boston Open Data Portal (API + bulk CSV)
- Property Assessment Data — Boston Assessing Department bulk download
- Student Housing Reports (2016–2024) — UAO submissions from participating universities
- SAM Address Dataset — Address standardization reference
- Neighborhood Shapefiles — Boston GIS Open Data

All datasets will be cleaned, joined via geocoded addresses or parcel IDs, and validated for consistency and temporal coverage.

## Data Analysis & Modeling

The project will begin with descriptive analytics:

- Compute district-level indicators (student share, violation rates, complaint density)
- Aggregate violation categories and severity scores
- Cross-tabulate 311 complaint frequency vs. violation severity
- Identify persistent clusters of student-linked violations using DBSCAN

If the modeling stage is reached:

- Train a logistic regression or gradient-boosted model on 2016–2021 data
- Validate on 2022 data, test on 2023–2024
- Target: AUROC ≥ 0.75 for predicting high-risk landlords

## Visualizations

Key outputs (finalized post-EDA):

- Student Share by District Over Time
- Top Violation Types Affecting Student Addresses
- Non-Compliant Landlords Map
- 311 Complaints vs. Violations Scatter
- Property Values vs. Student Density Trend
- Hotspot Clusters (DBSCAN Overlay on Map)

## Test Plan (TBD)

- Time-Aware Split: Train (2016–2021), Validate (2022), Test (2023–2024)
- Evaluation Metrics: Precision/Recall for compliance detection; R² for rent/value estimation
- Error Analysis: Review false positives/negatives for violation classification and geocoding accuracy.
