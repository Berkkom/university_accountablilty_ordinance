# University Accountability Ordinance (UAO) Project — Final Report  
**Boston University CS506 (Fall 2025)**  
**Date:** December 10, 2025  

**Final Presentation Video: https://youtu.be/IJW0LfH9E8I** <!-- TODO: paste YouTube link here -->

This project analyzes Boston’s University Accountability Ordinance (UAO) data, building/property code violations, 311 housing-related requests, standardized address (SAM) data, and university-reported student housing addresses to study housing quality and landlord non-compliance in student-dense areas of Boston.

---

## How to Build and Run the Code

### Required data (before running)

Raw data files are **not** included in this repository.  

To fully reproduce the analysis, download the following from the City of Boston open data portal (and provided UAO spreadsheet) and place them under `data/raw/`. You can obtain these by clicking the links in the **Data Sources** section below and saving/renaming the downloads to match the filenames listed here:

- `data/raw/violations_2016_2024.csv` 
- `data/raw/311_2016.csv`
- `data/raw/311_2017.csv`
- `data/raw/311_2018.csv`
- `data/raw/311_2019.csv`
- `data/raw/311_2020.csv`
- `data/raw/311_2021.csv`
- `data/raw/311_2022.csv`
- `data/raw/311_2023.csv`
- `data/raw/311_2024.csv`
- `data/raw/live_street_address_management_sam_addresses.csv`
- `data/raw/uao/uao_student_housing.csv`

The notebook expects these paths to exist. Once they are present, you can run the commands below.

### Set up the environment

This will execute `notebooks/UAO_midterm.ipynb` and write
`notebooks/UAO_midterm_executed.ipynb` with all cells run.

From the project root:

```bash
make venv
make run-notebook
make test

```
These commands will create the virtual environment, execute the main analysis notebook,
and run a small pytest-based smoke test suite.


Boston's **University Accountability Ordinance (UAO)** requires universities to annually report data about **off-campus student housing**. This project combines:

- building & property code violations,
- 311 housing-related service requests,
- standardized address (SAM) data, and
- UAO student housing address reports,

to study patterns of housing quality and landlord non-compliance in areas with high student density.

The project has three main components:

1. **Violation severity modeling** — classify violations as severe vs. non-severe using text and metadata.
2. **Future non-compliance prediction** — estimate the risk that a property will have a severe violation next year.
3. **Spatial & student-focused analysis** — identify clusters of high-risk properties and compare student vs. non-student addresses.

## Data Sources

All data were obtained from **Boston's Open Data Portal** or provided UAO spreadsheets and are stored locally under `data/raw/` (excluded from GitHub).

| Dataset | Description | Usage in this project |
|---------|-------------|----------------------|
| [Building and Property Violations (2016–2024)](https://data.boston.gov/dataset/building-and-property-violations1/resource/800a2663-1d6a-46e7-9356-bedb70f5332c) | Code violations reported to the Inspectional Services Department. | Core dataset: severity labels, temporal trends, property-level aggregation. |
| [311 Service Requests (2016–2024)](https://data.boston.gov/dataset/311-service-requests) | Public complaints and service requests. | Filtered to housing-related reasons; annual counts used to compare complaint volume vs. violations. |
| [SAM Addresses](https://data.boston.gov/dataset/live-street-address-management-sam-addresses) | Standardized address management (address IDs, geocoordinates, wards, neighborhoods). | Used to normalize addresses, join violations/UAO records, and obtain lat/lon + ward. |
| [UAO Student Housing Reports](https://docs.google.com/spreadsheets/d/11X4VvywkSodvvTk5kkQH7gtNPGovCgBq/edit?usp=drive_link&ouid=107346197263951251461&rtpof=true&sd=true) | University-reported off-campus student addresses by year and student type. | Mapped to SAM IDs to flag properties as student-linked and count students per property. |

## Data Processing

All processing steps are implemented in `notebooks/UAO_midterm.ipynb`. The main cleaned objects used downstream are `df_viol_c`, `df_311_housing`, `df_sam`, `student_prop`, `prop_year`, and `df_fut`.

### Violations (`df_viol_c`)

- Loaded ~17K building/property violation records (2016–2024).
- Standardized column names, date formats, and address fields.
- Extracted **year** from the violation date.
- Parsed free-text description and mapped violations into a coarse severity category:
  - **minor**, **moderate**, **severe**.
- Joined to SAM addresses to attach:
  - a stable property key (`sam_id`),
  - ward and (via SAM) neighborhood,
  - latitude/longitude for spatial analysis.
- Saved as cleaned DataFrame `df_viol_c` and reused across EDA and modeling.

### 311 Housing Requests (`df_311_housing`)

- Concatenated yearly 311 CSVs from `data/raw/311_*.csv` into a single table.
- Standardized column names and parsed an open date column → extracted year.
- Filtered to housing-related records using the 311 reason field (e.g., strings containing "HOUSING").
- Aggregated to `agg_311_year`: counts of housing-related 311 requests per year.

### SAM Addresses (`df_sam`)

- Loaded the SAM export from `data/raw/sam/live_street_address_management_sam_addresses.csv`.
- Standardized column names and kept:
  - `sam_address_id` (SAM ID),
  - `full_address`, `mailing_neighborhood`, `ward`, `zip_code`,
  - `point_x`, `point_y` (geographic coordinates).
- Used `sam_address_id` as a property identifier and attached it to violations and UAO records.

### UAO Student Housing (`df_uao_raw` → `student_prop`)

- Loaded UAO off-campus housing data from `data/raw/uao/uao_student_housing.csv`.
- Columns include:
  - `6a. street #`, `6b. street name`, `6c. street suffix`, `6d. unit #`, `6e. zip`,
  - student type (undergrad/grad, FT/PT),
  - university name, year.
- Constructed a normalized address key from street number, street name/suffix, unit, and ZIP.
- Constructed a similar normalized key on SAM addresses and joined UAO → SAM.
- Achieved a match rate of ~97% from UAO rows to SAM IDs.
- Aggregated to a property-level student table `student_prop` with:
  - `prop_id` (SAM ID),
  - `n_students` per property,
  - `is_student_address` (Boolean flag).

### Property–Year Panel (`prop_year`) and Future Label (`df_fut`)

From `df_viol_c`, created a panel of violations per property and year:

- Chose `sam_id` as the property key (`prop_id` in the panel).
- Aggregated to `prop_year` with, for each (`prop_id`, `year`):
  - `n_viol`: total violations,
  - `n_severe`, `n_moderate`, `n_minor`,
  - dominant ward,
  - `prop_severe` = `n_severe` / `n_viol`.

To set up a future non-compliance label:

- Sorted `prop_year` by `prop_id`, `year`.
- For each property, created `n_severe_next_year` using `.groupby("prop_id")["n_severe"].shift(-1)`.
- Dropped rows where the next year is missing (final year for each property).
- Defined binary target:
  - `y_future_severe` = 1 if `n_severe_next_year > 0`, else 0.
- The resulting panel is stored as `df_fut`.

## Exploratory Visualizations

All visualizations are produced inside the notebook and can be reproduced via `make run-notebook`.

### Violation Trends and Types

**Violations per Year (2016–2024)**

Line plot of total violations per year, showing:
- a peak around the late 2010s and
- a decline in total violations in more recent years.

**Top Violation Descriptions**

Bar chart of the most frequent violation descriptions, highlighting categories such as:
- *Failure to Obtain Permit*,
- *Unsafe and Dangerous*,
- *Maintenance*.

**Severity Distribution**

Overall distribution of minor, moderate, and severe violations.

Most violations are **minor**, with roughly ~10% classified as **severe**.

### Violations vs. 311 Housing Requests

Computed annual counts of:
- building violations (`n_violations`),
- housing-related 311 requests (`n_311_requests`).

Overlaid them on a dual-axis plot (violations on one y-axis, 311 on the other).

This gives a high-level view of whether complaint volume and observed violations move together over time.

## Modeling

### Text-Based Severity Classifier

We trained a logistic regression classifier to predict whether a violation is severe (`is_severe` = 1) based on:
- `year` (numeric),
- `ward` (categorical),
- `description` (free text).

**Pipeline:**
- Numeric (`year`): median imputation + `StandardScaler`.
- Categorical (`ward`): most-frequent imputation + `OneHotEncoder`.
- Text (`description`): `TfidfVectorizer` with 1–2 grams and up to 3,000 features.
- Combined with a `ColumnTransformer`, then fed to:
  - `LogisticRegression(solver="saga", class_weight="balanced", max_iter=5000)`.

**Train/Test:**
- Standard 75%/25% split (stratified by `is_severe`).

The classifier achieves very strong discrimination (high AUROC and PR-AUC), confirming that textual descriptions encode severity signals like "UNSAFE", "FIRE", "STRUCTURAL", etc., versus more routine maintenance language.

### Generalization Across Years and Wards

To avoid overfitting to a specific time or neighborhood, we ran two types of robustness checks:

**Time generalization (rolling year cutoff):**
- For each year cutoff, train on violations <= cutoff and test on violations > cutoff.
- Skipped very small or degenerate splits (e.g., when test data had only one class).
- The model maintains strong AUROC across different train/test year splits, indicating temporal stability.

**Ward-level holdout:**
- For each ward, train on all other wards, test on the held-out ward.
- Again, skipped wards with too few severe cases.
- Performance remains high for most wards, suggesting that the text model is not over-specialized to a single geographic area.

### Future Non-Compliance Model (Property–Year Level)

We modeled the probability that a property will experience a severe violation in the next year:

**Input features** (from `prop_year`):
- `n_viol`, `n_severe`, `n_minor`, `prop_severe`, `year` (numeric),
- `ward` (categorical).

**Target:**
- `y_future_severe` from `df_fut` (whether `n_severe_next_year > 0`).

**Pipeline:**
- Numeric features: median impute + `StandardScaler`.
- Categorical (`ward`): most-frequent impute + `OneHotEncoder`.
- Classifier: `LogisticRegression(class_weight="balanced", max_iter=1000)`.

**Train/test split:**
- 75%/25% with stratification by `y_future_severe`.

The resulting model produces reasonable AUROC and precision/recall, showing that past severity and violation patterns are informative about next-year risk, but not perfectly predictive—highlighting the value (and limits) of using historical administrative data for forecasting.

## Spatial Analysis and DBSCAN Clustering

Using `df_viol_c` joined to SAM coordinates:

- Aggregated to a property-level geo table (`prop_geo`) with:
  - median lat/lon per property,
  - counts of total and severe violations,
  - `prop_severe` share.
- Focused on high-risk properties:
  - `n_severe >= 1`.
- Filtered to a reasonable Boston bounding box:
  - `lat ∈ [42.0, 42.6]`, `lon ∈ [-71.3, -70.8]`.
- Ran DBSCAN on standardized coordinates (lat, lon):
  - Standardized features: `StandardScaler()` on `[lat, lon]`.
  - DBSCAN parameters (in standardized units):
    - `eps = 0.18`, `min_samples = 25`.
  - This corresponds roughly to clusters at the scale of a few city blocks, grouping high-risk properties that are spatially close together.

**Visualizations:**
- Scatter plot of clusters in (lon, lat) space:
  - each cluster colored distinctly,
  - noise points (cluster = -1) plotted in black.
- Basemap overlay using `geopandas` + `contextily`:
  - points projected to Web Mercator (EPSG:3857),
  - plotted on a CartoDB Positron basemap,
  - visually highlighting pockets of severe violations over the city map.

These clusters can be interpreted as localized pockets of non-compliance, potentially pointing to particularly problematic blocks or landlord portfolios.

## Student Housing Integration (UAO + Violations)

Using the `student_prop` table (UAO addresses matched to SAM), we enriched both the violation-level and property-year tables:

**Violation level** (`df_viol_with_student`):
- Each violation row is tagged with:
  - `n_students` at that property,
  - `is_student_address` (True/False).

**Property–year level** (`prop_year_student` & `df_fut_student`):
- Each property/year panel row and each future-risk row contains:
  - `n_students`,
  - `is_student_address`.

We then computed and plotted:

**Current severe share by student flag:**
- At the violation level:
  - group by `is_student_address`,
  - compute the rate of `severity == "severe"`.

**Future severe risk by student flag:**
- At the property/year level (`df_fut_student`):
  - group by `is_student_address`,
  - compute mean of `y_future_severe`.

Bar plots compare:
- **Current severe rate**: student addresses vs. non-student addresses.
- **Next-year severe risk**: student vs. non-student properties.

This provides an initial, data-driven view of whether student-linked properties experience more severe issues now and/or in the near future.

## Compliance Risk by Ward

To make ward-based risk plots more interpretable:

- Computed for each ward:
  - **Current severe share**: violation-level `is_severe` rate by ward.
  - **Future severe risk**: mean `y_future_severe` per ward from `df_fut`.
- Combined into a single `risk_ward` table, then labeled wards using SAM's `MAILING_NEIGHBORHOOD` and a small manual mapping:
  - E.g., W21 – Allston/Brighton, W22 – Mission Hill/JP, etc.
- For some wards without clear neighborhood labels in SAM, used manual descriptive names.
- Plotted a grouped bar chart with:
  - x-axis: labeled wards (e.g., W21 – Allston/Brighton),
  - bars: current severe share vs. future severe risk.

This plot acts as a compliance risk "heatmap" by ward, showing which parts of the city appear more at risk both now and in the near term.

## Testing and CI

To satisfy the project requirement for testing and CI:

**Tests:**
- Simple pytest-based smoke tests live under `tests/`, e.g.:
  - checking that `df_viol_c` loads and has expected columns,
  - verifying that the severity classifier pipeline can be constructed and fit on a small sample without error.

**GitHub Actions workflow:**
- A workflow under `.github/workflows/tests.yml` (or similar) runs:
  - `make venv`
  - `make test`
- on pushes / pull requests, ensuring that the core analysis and pipelines remain runnable.

(If you change your test or workflow filenames, update this description accordingly.)

## Key Findings and Takeaways

1. **Text descriptions are highly informative for severity.**
   - A simple logistic regression with TF-IDF features can almost perfectly separate severe vs. non-severe violations, highlighting the value of free-text fields in administrative data.

2. **The severity model is robust across time and space.**
   - Year-based and ward-based holdout tests show that the model generalizes reasonably well to future years and to unseen wards, rather than memorizing particular phrases from a single time or neighborhood.

3. **Past severe behavior predicts future risk.**
   - Properties with a history of severe violations (and higher `prop_severe` shares) have elevated risk of severe violations in the next year.

4. **High-risk properties cluster spatially.**
   - DBSCAN identifies clusters of high-risk properties at the scale of a few city blocks, which could be used by inspectors to prioritize proactive inspections.

5. **Student-linked properties can be systematically analyzed.**
   - By linking UAO student housing addresses to SAM IDs and then to violations, we can:
     - quantify how many student addresses are associated with severe violations, and
     - compare current and future severe risk between student and non-student properties.

## Limitations and Future Work

**Data coverage and labeling:**
- Severity labels are derived from text and/or coarse categories; ground truth about actual risk may be more nuanced.

**Property assessments and ownership:**
- Integrating property assessment data (owners, assessed values) could reveal whether certain landlords or asset tiers are systematically higher risk.

**Richer spatial models:**
- More sophisticated spatial models (e.g., spatial autocorrelation, graph-based methods) could better capture spillover effects between nearby properties.

**Interactive dashboard:**
- An interactive dashboard (e.g. in Dash/Streamlit) could help policymakers and inspectors explore high-risk clusters, wards, and student-linked properties more intuitively.

Despite these limitations, the current pipeline demonstrates that open city data + UAO student reports can be joined, modeled, and visualized to support a data-driven view of housing quality and compliance risk in student-dense neighborhoods.
