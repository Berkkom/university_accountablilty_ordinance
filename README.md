from pathlib import Path

readme_content = """# 🏙️ University Accountability Ordinance (UAO) Project — Midterm Report  
**Boston University CS506 (Fall 2025)**  
**Date:** October 27, 2025  

📺 **Presentation Video:** [Add YouTube Link Here]  

---

## 1. Project Overview

Boston’s **University Accountability Ordinance (UAO)** requires universities to annually report data about **off-campus student housing**.  
This project analyzes public data from 2016–2024 to understand student presence in Boston’s rental market, housing condition trends, and potential landlord non-compliance patterns.

For the midterm milestone, the focus is on **building and property violation data** — exploring trends, common violation types, and building a preliminary text-based model to classify violation severity.

---

## 2. Data Sources

All data were obtained from **Boston’s Open Data Portal** and are stored locally (excluded from GitHub per course policy).

| Dataset | Description | Source |
|----------|--------------|--------|
| Building and Property Violations (2016–2024) | Code violations reported to the Inspectional Services Department. | [Boston Open Data Portal](https://data.boston.gov/dataset/building-and-property-violations1) |
| 311 Service Requests *(planned)* | Public complaints and service requests. | [Boston 311 API](https://data.boston.gov/dataset/311-service-requests) |
| Property Assessments *(planned)* | Ownership and property value data. | [Boston Assessing Department](https://data.boston.gov/dataset/property-assessment) |
| SAM Addresses *(planned)* | Standardized address mapping. | [Boston GIS](https://data.boston.gov/dataset/standardized-addresses) |
| UAO Student Housing Reports *(planned)* | University-provided student address data. | City of Boston UAO filings |

All raw files are stored under `notebooks/data/raw/` and listed in `.gitignore`.

---

## 3. Data Processing

Work completed so far:
- Loaded ~17K building violation records (2016–2024).  
- Cleaned and standardized column names, address fields, and timestamps.  
- Extracted **year** from violation date fields.  
- Parsed violation **descriptions** and assigned a **severity category** (minor, moderate, severe).  
- Computed summary statistics for temporal and categorical trends.  
- Generated clean DataFrame (`df_viol_c`) used in exploratory and modeling sections.  

---

## 4. Preliminary Visualizations

### Violation Counts by Year (2016–2024)
Shows a clear decline in total reported violations since 2018.

### Top 15 Violation Descriptions
Most frequent categories include:
- *Failure to Obtain Permit*  
- *Unsafe and Dangerous*  
- *Work Without Permit*  

### Violation Severity Distribution
Majority of violations are **minor**, with approximately **10% classified as severe**.

---

## 5. Modeling Approach

A **logistic regression classifier** was trained to predict violation severity (`severe` vs. others) using textual and categorical features.

| Step | Description |
|------|--------------|
| **Input Features** | `year`, `ward`, and `description` |
| **Text Processing** | TF-IDF vectorization (1–2 n-grams, 3,000 features) |
| **Preprocessing** | Imputation, scaling, and one-hot encoding via `ColumnTransformer` |
| **Model** | Logistic Regression (`solver="saga"`, `max_iter=5000`, `class_weight="balanced"`) |
| **Split** | 75% training / 25% testing (stratified) |

---

## 6. Preliminary Results

| Metric | Value |
|---------|--------|
| Accuracy | **0.996** |
| Precision (Severe) | **0.989** |
| Recall (Severe) | **0.973** |
| AUROC | **1.000** |
| PR-AUC | **0.997** |

The text-based model achieved **near-perfect predictive performance**.  
This indicates that violation descriptions contain highly discriminative language for severity (e.g., “UNSAFE STRUCTURE”, “FIRE”, “ELECTRICAL HAZARD”).  
Future work will validate whether this performance generalizes across different years and address categories.

---

## 7. Next Steps

### Data Integration
- Add **311 Service Requests** and **Property Assessment** data for richer context.  
- Join with **UAO student housing reports** to identify student-linked addresses.  
- Normalize address fields using **SAM reference data**.

### Modeling
- Evaluate generalization across years and neighborhoods.  
- Incorporate tree-based models (Gradient Boosting / XGBoost).  
- Introduce **spatial clustering (DBSCAN)** for non-compliant landlord detection.  
- Extend classification to predict *future non-compliance probability*.

### Final Deliverables
- Interactive geospatial dashboard.  
- Compliance risk heatmap by neighborhood.  
- Full summary linking **student density** to **violation severity and landlord patterns**.

---

## 8. Repository Structure

