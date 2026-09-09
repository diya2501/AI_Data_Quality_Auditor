import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

print("===================================")
print("   AI DATA QUALITY AUDITOR")
print("===================================")

# Load dirty dataset
df = pd.read_csv("AI_Auditor_Input_Dirty_1000.csv")

print("\nDataset successfully loaded!")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# Display first 10 records
print("\nFirst 10 Records:")
print(df.head(10))

# Dataset information
print("\nDataset Information:")
df.info()

# Missing value detection
missing_values = df.isnull().sum()

print("\nMissing Values:")
print(missing_values[missing_values > 0])

# Duplicate detection
duplicate_count = df.duplicated().sum()

print("\nTotal Duplicate Records:", duplicate_count)

# Basic Audit Summary
audit_summary = pd.DataFrame({
    "Metric": [
        "Total Rows",
        "Total Columns",
        "Total Missing Values",
        "Duplicate Records"
    ],
    "Count": [
        df.shape[0],
        df.shape[1],
        df.isnull().sum().sum(),
        duplicate_count
    ]
})

print("\n========== AUDIT SUMMARY ==========")
print(audit_summary)

# ==========================================
# INVALID EMAIL DETECTION
# ==========================================

email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

invalid_email_mask = (
    df["email"].notna() &
    ~df["email"].astype(str).str.match(email_pattern)
)

invalid_emails = df[invalid_email_mask]

print("\n========== INVALID EMAIL AUDIT ==========")
print("Invalid Email Count:", len(invalid_emails))

if len(invalid_emails) > 0:
    print("\nInvalid Email Records:")
    print(invalid_emails[["order_id", "customer_name", "email"]])

# ==========================================
# INVALID PHONE DETECTION
# ==========================================

phone_pattern = r'^[6-9][0-9]{9}$'

invalid_phone_mask = (
    df["phone"].notna() &
    ~df["phone"].astype(str).str.match(phone_pattern)
)

invalid_phones = df[invalid_phone_mask]

print("\n========== INVALID PHONE AUDIT ==========")
print("Invalid Phone Count:", len(invalid_phones))

if len(invalid_phones) > 0:
    print("\nInvalid Phone Records:")
    print(invalid_phones[["order_id", "customer_name", "phone"]])

# ==========================================
# INVALID POSTAL CODE DETECTION
# ==========================================

postal_pattern = r'^[1-9][0-9]{5}$'

invalid_postal_mask = (
    df["postal_code"].notna() &
    ~df["postal_code"].astype(str).str.match(postal_pattern)
)

invalid_postal_codes = df[invalid_postal_mask]

print("\n========== INVALID POSTAL CODE AUDIT ==========")
print("Invalid Postal Code Count:", len(invalid_postal_codes))

if len(invalid_postal_codes) > 0:
    print("\nInvalid Postal Code Records:")
    print(
        invalid_postal_codes[
            ["order_id", "city", "state", "postal_code"]
        ]
    )

# ==========================================
# INVALID DATE DETECTION
# ==========================================

# Convert order_date into proper date format
df["parsed_date"] = pd.to_datetime(
    df["order_date"],
    errors="coerce",
    dayfirst=True
)

# Invalid dates become NaT
invalid_date_mask = (
    df["order_date"].notna() &
    df["parsed_date"].isna()
)

invalid_dates = df[invalid_date_mask]

print("\n========== INVALID DATE AUDIT ==========")
print("Invalid Date Count:", len(invalid_dates))

if len(invalid_dates) > 0:
    print("\nInvalid Date Records:")
    print(
        invalid_dates[
            ["order_id", "order_date"]
        ]
    )

# ==========================================
# INVALID PRICE DETECTION
# ==========================================

# Convert unit price to numeric
df["parsed_price"] = pd.to_numeric(
    df["unit_price_inr"],
    errors="coerce"
)

# Detect zero, negative and non-numeric prices
invalid_price_mask = (
    df["unit_price_inr"].notna() &
    (
        df["parsed_price"].isna() |
        (df["parsed_price"] <= 0)
    )
)

invalid_prices = df[invalid_price_mask]

print("\n========== INVALID PRICE AUDIT ==========")
print("Invalid Price Count:", len(invalid_prices))

if len(invalid_prices) > 0:
    print("\nInvalid Price Records:")
    print(
        invalid_prices[
            ["order_id", "product_name", "unit_price_inr"]
        ]
    )

# ==========================================
# INVALID QUANTITY DETECTION
# ==========================================

# Convert quantity to numeric
df["parsed_quantity"] = pd.to_numeric(
    df["quantity"],
    errors="coerce"
)

# Detect zero, negative and non-numeric quantities
invalid_quantity_mask = (
    df["quantity"].notna() &
    (
        df["parsed_quantity"].isna() |
        (df["parsed_quantity"] <= 0)
    )
)

invalid_quantities = df[invalid_quantity_mask]

print("\n========== INVALID QUANTITY AUDIT ==========")
print("Invalid Quantity Count:", len(invalid_quantities))

if len(invalid_quantities) > 0:
    print("\nInvalid Quantity Records:")
    print(
        invalid_quantities[
            ["order_id", "product_name", "quantity"]
        ]
    )


# ==========================================
# QUANTITY OUTLIER DETECTION
# ==========================================

# For this project, quantity above 10 is considered unusual
quantity_outlier_mask = (
    df["parsed_quantity"].notna() &
    (df["parsed_quantity"] > 10)
)

quantity_outliers = df[quantity_outlier_mask]

print("\n========== QUANTITY OUTLIER AUDIT ==========")
print("Quantity Outlier Count:", len(quantity_outliers))

if len(quantity_outliers) > 0:
    print("\nQuantity Outlier Records:")
    print(
        quantity_outliers[
            ["order_id", "product_name", "quantity"]
        ]
    )

# ==========================================
# PRICE OUTLIER DETECTION USING IQR
# ==========================================

# Remove missing values for calculation
price_data = df["parsed_price"].dropna()

# Calculate Q1 and Q3
Q1 = price_data.quantile(0.25)
Q3 = price_data.quantile(0.75)

# Calculate IQR
IQR = Q3 - Q1

# Calculate lower and upper limits
lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR

# Detect price outliers
price_outlier_mask = (
    df["parsed_price"].notna() &
    (
        (df["parsed_price"] < lower_limit) |
        (df["parsed_price"] > upper_limit)
    )
)

price_outliers = df[price_outlier_mask]

print("\n========== PRICE OUTLIER AUDIT ==========")
print("Q1:", Q1)
print("Q3:", Q3)
print("IQR:", IQR)
print("Lower Limit:", lower_limit)
print("Upper Limit:", upper_limit)
print("Price Outlier Count:", len(price_outliers))

if len(price_outliers) > 0:
    print("\nPrice Outlier Records:")
    print(
        price_outliers[
            ["order_id", "product_name", "unit_price_inr"]
        ]
    )

# ==========================================
# CITY-STATE MISMATCH DETECTION
# ==========================================

city_state_mapping = {
    "Nagpur": "Maharashtra",
    "Mumbai": "Maharashtra",
    "Pune": "Maharashtra",
    "Delhi": "Delhi",
    "Bengaluru": "Karnataka",
    "Hyderabad": "Telangana",
    "Ahmedabad": "Gujarat",
    "Jaipur": "Rajasthan",
    "Kolkata": "West Bengal",
    "Chennai": "Tamil Nadu"
}

def check_city_state(row):
    city = str(row["city"]).strip()
    state = str(row["state"]).strip()

    if city in city_state_mapping:
        return state != city_state_mapping[city]

    return False


city_state_mask = df.apply(check_city_state, axis=1)

city_state_errors = df[city_state_mask]

print("\n========== CITY-STATE MISMATCH AUDIT ==========")
print("City-State Mismatch Count:", len(city_state_errors))

if len(city_state_errors) > 0:
    print("\nCity-State Mismatch Records:")
    print(
        city_state_errors[
            ["order_id", "city", "state"]
        ]
    )

# ==========================================
# PRODUCT-CATEGORY MISMATCH DETECTION
# ==========================================

product_category_mapping = {
    "Wireless Mouse": "Electronics",
    "Bluetooth Speaker": "Electronics",
    "Cotton Kurta": "Fashion",
    "Running Shoes": "Fashion",
    "Water Bottle": "Home",
    "Bedsheet Set": "Home",
    "Face Serum": "Beauty",
    "Shampoo": "Beauty",
    "Notebook Pack": "Stationery",
    "Desk Organizer": "Stationery"
}


def check_product_category(row):
    product = str(row["product_name"]).strip()
    category = str(row["category"]).strip()

    if product in product_category_mapping:
        return category != product_category_mapping[product]

    return False


product_category_mask = df.apply(
    check_product_category,
    axis=1
)

product_category_errors = df[product_category_mask]

print("\n========== PRODUCT-CATEGORY MISMATCH AUDIT ==========")
print(
    "Product-Category Mismatch Count:",
    len(product_category_errors)
)

if len(product_category_errors) > 0:
    print("\nProduct-Category Mismatch Records:")
    print(
        product_category_errors[
            ["order_id", "product_name", "category"]
        ]
    )

# ==========================================
# CUSTOMER CONSISTENCY DETECTION
# ==========================================

customer_consistency = (
    df.groupby("customer_id")
    .agg(
        unique_names=("customer_name", "nunique"),
        unique_emails=("email", "nunique"),
        unique_phones=("phone", "nunique")
    )
    .reset_index()
)

# Customers having different details
inconsistent_customers = customer_consistency[
    (customer_consistency["unique_names"] > 1) |
    (customer_consistency["unique_emails"] > 1) |
    (customer_consistency["unique_phones"] > 1)
]

print("\n========== CUSTOMER CONSISTENCY AUDIT ==========")
print(
    "Customers with inconsistent details:",
    len(inconsistent_customers)
)

if len(inconsistent_customers) > 0:
    print("\nInconsistent Customer IDs:")
    print(inconsistent_customers)

    print("\nDetailed Records:")

    inconsistent_ids = inconsistent_customers["customer_id"]

    print(
        df[df["customer_id"].isin(inconsistent_ids)][
            [
                "customer_id",
                "customer_name",
                "email",
                "phone"
            ]
        ].sort_values("customer_id")
    )

# ==========================================
# SPELLING & CAPITALIZATION CHECK
# ==========================================

def normalize_text(value):
    if pd.isna(value):
        return ""
    
    return (
        str(value)
        .strip()
        .lower()
    )


columns_to_check = [
    "customer_name",
    "city",
    "state",
    "product_name",
    "category"
]

print("\n========== SPELLING & CAPITALIZATION AUDIT ==========")

for column in columns_to_check:

    # Original values
    original_values = df[column].dropna().astype(str).str.strip()

    # Normalized values
    normalized_values = original_values.str.lower()

    # Find values where capitalization/spacing differs
    consistency_check = pd.DataFrame({
        "Original": original_values,
        "Normalized": normalized_values
    })

    differences = consistency_check[
        consistency_check["Original"] != consistency_check["Normalized"]
    ]

    print(f"\nColumn: {column}")
    print("Potential formatting differences:", len(differences))

    if len(differences) > 0:
        print(differences.head(10))

# ==========================================
# COMPLETE ERROR REPORT
# ==========================================

error_report = pd.DataFrame({
    "Error Type": [
        "Missing Values",
        "Duplicate Records",
        "Invalid Emails",
        "Invalid Phones",
        "Invalid Postal Codes",
        "Invalid Dates",
        "Invalid Prices",
        "Invalid Quantities",
        "Quantity Outliers",
        "Price Outliers",
        "City-State Mismatch",
        "Product-Category Mismatch",
        "Customer Consistency Errors"
    ],

    "Error Count": [
        df.isnull().sum().sum(),
        duplicate_count,
        len(invalid_emails),
        len(invalid_phones),
        len(invalid_postal_codes),
        len(invalid_dates),
        len(invalid_prices),
        len(invalid_quantities),
        len(quantity_outliers),
        len(price_outliers),
        len(city_state_errors),
        len(product_category_errors),
        len(inconsistent_customers)
    ]
})

print("\n")
print("==========================================")
print("        COMPLETE DATA ERROR REPORT")
print("==========================================")

print(error_report)

# ==========================================
# AI-STYLE CORRECTION SUGGESTIONS
# ==========================================

corrections = []

# ------------------------------------------
# 1. Email Correction Suggestions
# ------------------------------------------

for index, row in invalid_emails.iterrows():

    email = str(row["email"]).strip()

    suggestion = ""

    # Common email domain corrections
    if email.endswith("@gmail"):
        suggestion = email + ".com"

    elif email.endswith("@yahoo"):
        suggestion = email + ".com"

    elif email.endswith("@hotmail"):
        suggestion = email + ".com"

    elif "@" not in email:
        suggestion = "Review email manually"

    else:
        suggestion = "Review email format"

    corrections.append({
        "order_id": row["order_id"],
        "Column": "email",
        "Original Value": row["email"],
        "Suggested Value": suggestion,
        "Reason": "Invalid email format"
    })


# ------------------------------------------
# 2. City-State Correction Suggestions
# ------------------------------------------

for index, row in city_state_errors.iterrows():

    city = str(row["city"]).strip()

    if city in city_state_mapping:

        suggested_state = city_state_mapping[city]

        corrections.append({
            "order_id": row["order_id"],
            "Column": "state",
            "Original Value": row["state"],
            "Suggested Value": suggested_state,
            "Reason": "City-State mismatch"
        })


# ------------------------------------------
# 3. Product-Category Correction Suggestions
# ------------------------------------------

for index, row in product_category_errors.iterrows():

    product = str(row["product_name"]).strip()

    if product in product_category_mapping:

        suggested_category = product_category_mapping[product]

        corrections.append({
            "order_id": row["order_id"],
            "Column": "category",
            "Original Value": row["category"],
            "Suggested Value": suggested_category,
            "Reason": "Product-Category mismatch"
        })


# ------------------------------------------
# Create Correction Report
# ------------------------------------------

correction_report = pd.DataFrame(corrections)

print("\n==========================================")
print("       AI CORRECTION SUGGESTIONS")
print("==========================================")

if len(correction_report) > 0:
    print(correction_report.to_string(index=False))
else:
    print("No correction suggestions generated.")

# ==========================================
# AUTOMATIC DATA CLEANING
# ==========================================

cleaned_df = df.copy()

# ------------------------------------------
# 1. Fix Email Values
# ------------------------------------------

for index, row in invalid_emails.iterrows():

    email = str(row["email"]).strip()

    if email.endswith("@gmail"):
        cleaned_df.loc[index, "email"] = email + ".com"

    elif email.endswith("@yahoo"):
        cleaned_df.loc[index, "email"] = email + ".com"

    elif email.endswith("@hotmail"):
        cleaned_df.loc[index, "email"] = email + ".com"


# ------------------------------------------
# 2. Fix City-State Mismatch
# ------------------------------------------

for index, row in city_state_errors.iterrows():

    city = str(row["city"]).strip()

    if city in city_state_mapping:
        cleaned_df.loc[index, "state"] = city_state_mapping[city]


# ------------------------------------------
# 3. Fix Product-Category Mismatch
# ------------------------------------------

for index, row in product_category_errors.iterrows():

    product = str(row["product_name"]).strip()

    if product in product_category_mapping:
        cleaned_df.loc[index, "category"] = (
            product_category_mapping[product]
        )


# ------------------------------------------
# 4. Standardize Text Formatting
# ------------------------------------------

text_columns = [
    "customer_name",
    "city",
    "state",
    "product_name",
    "category"
]

for column in text_columns:

    cleaned_df[column] = cleaned_df[column].apply(
        lambda x: x.strip().title()
        if pd.notna(x)
        else x
    )


# ------------------------------------------
# 5. Remove Exact Duplicate Records
# ------------------------------------------

before_duplicates = len(cleaned_df)

cleaned_df = cleaned_df.drop_duplicates()

after_duplicates = len(cleaned_df)

duplicates_removed = before_duplicates - after_duplicates


# ------------------------------------------
# 6. Remove Temporary Columns
# ------------------------------------------

temporary_columns = [
    "parsed_date",
    "parsed_price",
    "parsed_quantity"
]

cleaned_df = cleaned_df.drop(
    columns=temporary_columns,
    errors="ignore"
)


# ------------------------------------------
# Save Clean Dataset
# ------------------------------------------

cleaned_df.to_csv(
    "cleaned_orders.csv",
    index=False
)

print("\n==========================================")
print("       AUTOMATIC DATA CLEANING")
print("==========================================")

print("Original Rows:", len(df))
print("Cleaned Rows:", len(cleaned_df))
print("Duplicate Rows Removed:", duplicates_removed)

print("\nCleaned dataset saved successfully!")
print("File: cleaned_orders.csv")

# ==========================================
# BEFORE VS AFTER COMPARISON
# ==========================================

print("\n==========================================")
print("        BEFORE VS AFTER COMPARISON")
print("==========================================")

# BEFORE cleaning
before_missing = df.isnull().sum().sum()
before_duplicates = df.duplicated().sum()

# AFTER cleaning
after_missing = cleaned_df.isnull().sum().sum()
after_duplicates = cleaned_df.duplicated().sum()

comparison = pd.DataFrame({
    "Metric": [
        "Total Rows",
        "Total Columns",
        "Missing Values",
        "Duplicate Records"
    ],

    "Before Cleaning": [
        len(df),
        len(df.columns),
        before_missing,
        before_duplicates
    ],

    "After Cleaning": [
        len(cleaned_df),
        len(cleaned_df.columns),
        after_missing,
        after_duplicates
    ]
})

print(comparison)

# ==========================================
# DATA QUALITY SCORE
# ==========================================

print("\n==========================================")
print("          DATA QUALITY SCORE")
print("==========================================")

total_rows = len(df)

# BEFORE CLEANING
before_missing_rate = (
    df.isnull().sum().sum() /
    (len(df) * len(df.columns))
) * 100

before_duplicate_rate = (
    df.duplicated().sum() /
    len(df)
) * 100

before_error_count = (
    len(invalid_emails) +
    len(invalid_phones) +
    len(invalid_postal_codes) +
    len(invalid_dates) +
    len(invalid_prices) +
    len(invalid_quantities) +
    len(quantity_outliers) +
    len(price_outliers) +
    len(city_state_errors) +
    len(product_category_errors) +
    len(inconsistent_customers)
)

# AFTER CLEANING
after_missing_rate = (
    cleaned_df.isnull().sum().sum() /
    (len(cleaned_df) * len(cleaned_df.columns))
) * 100

after_duplicate_rate = (
    cleaned_df.duplicated().sum() /
    len(cleaned_df)
) * 100

# Calculate scores
before_score = max(
    0,
    100 - (
        before_missing_rate * 0.30 +
        before_duplicate_rate * 0.20 +
        min(before_error_count / total_rows * 100, 100) * 0.50
    )
)

after_score = max(
    0,
    100 - (
        after_missing_rate * 0.30 +
        after_duplicate_rate * 0.20
    )
)

print("Before Cleaning Score:", round(before_score, 2), "/ 100")
print("After Cleaning Score:", round(after_score, 2), "/ 100")

print(
    "Quality Improvement:",
    round(after_score - before_score, 2),
    "points"
)

# ==========================================
# SAVE COMPLETE ERROR REPORT
# ==========================================

error_report.to_csv(
    "Complete_Error_Report.csv",
    index=False
)

print("\nComplete error report saved successfully!")
print("File: Complete_Error_Report.csv")

# ==========================================
# ERROR DISTRIBUTION CHART
# ==========================================

chart_data = error_report[
    error_report["Error Count"] > 0
].copy()

plt.figure(figsize=(12, 7))

plt.bar(
    chart_data["Error Type"],
    chart_data["Error Count"]
)

plt.title("Data Quality Errors Detected")
plt.xlabel("Error Type")
plt.ylabel("Number of Errors")

plt.xticks(
    rotation=60,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    "Error_Distribution_Chart.png",
    dpi=300
)

plt.show()

print("\nError distribution chart saved successfully!")
print("File: Error_Distribution_Chart.png")

# ==========================================
# BEFORE VS AFTER CHART
# ==========================================

metrics = [
    "Missing Values",
    "Duplicate Records"
]

before_values = [
    before_missing,
    before_duplicates
]

after_values = [
    after_missing,
    after_duplicates
]

x = np.arange(len(metrics))
width = 0.35

plt.figure(figsize=(9, 6))

plt.bar(
    x - width / 2,
    before_values,
    width,
    label="Before Cleaning"
)

plt.bar(
    x + width / 2,
    after_values,
    width,
    label="After Cleaning"
)

plt.xticks(x, metrics)
plt.ylabel("Count")
plt.title("Before vs After Data Cleaning")

plt.legend()
plt.tight_layout()

plt.savefig(
    "Before_After_Chart.png",
    dpi=300
)

plt.show()

print("Before-after chart saved successfully!")
print("File: Before_After_Chart.png")

# ==========================================
# SAVE CORRECTION SUGGESTIONS
# ==========================================

correction_report.to_csv(
    "AI_Correction_Suggestions.csv",
    index=False
)

print("\nAI correction suggestions saved successfully!")
print("File: AI_Correction_Suggestions.csv")


# ==========================================
# SAVE BEFORE-AFTER COMPARISON
# ==========================================

comparison.to_csv(
    "Before_After_Comparison.csv",
    index=False
)

print("\nBefore-after comparison saved successfully!")
print("File: Before_After_Comparison.csv")

# ==========================================
# SAVE DATA QUALITY SCORE REPORT
# ==========================================

quality_score_report = pd.DataFrame({
    "Metric": [
        "Before Cleaning Score",
        "After Cleaning Score",
        "Quality Improvement"
    ],
    "Score": [
        round(before_score, 2),
        round(after_score, 2),
        round(after_score - before_score, 2)
    ]
})

quality_score_report.to_csv(
    "Data_Quality_Score_Report.csv",
    index=False
)

print("\nData quality score report saved successfully!")
print("File: Data_Quality_Score_Report.csv")

# ==========================================
# ML-BASED ANOMALY DETECTION
# ==========================================

from sklearn.ensemble import IsolationForest

print("\n==========================================")
print("       ML ANOMALY DETECTION")
print("==========================================")

# Select numerical features
ml_data = df[[
    "parsed_price",
    "parsed_quantity"
]].copy()

# Replace missing values with median values
ml_data["parsed_price"] = ml_data["parsed_price"].fillna(
    ml_data["parsed_price"].median()
)

ml_data["parsed_quantity"] = ml_data["parsed_quantity"].fillna(
    ml_data["parsed_quantity"].median()
)

# Create Isolation Forest model
model = IsolationForest(
    contamination="auto",
    random_state=42
)

# Train model and predict anomalies
df["ml_anomaly"] = model.fit_predict(ml_data)

# -1 = anomaly
#  1 = normal

ml_anomalies = df[df["ml_anomaly"] == -1].copy()

print("ML Anomalies Detected:", len(ml_anomalies))

if len(ml_anomalies) > 0:

    print("\nML Anomaly Records:")

    print(
        ml_anomalies[
            [
                "order_id",
                "product_name",
                "quantity",
                "unit_price_inr"
            ]
        ].head(20)
    )


# ==========================================
# SAVE ML ANOMALY REPORT
# ==========================================

ml_anomaly_report = ml_anomalies[
    [
        "order_id",
        "product_name",
        "quantity",
        "unit_price_inr"
    ]
].copy()

ml_anomaly_report["Detection Method"] = "Isolation Forest"
ml_anomaly_report["Reason"] = "Unusual combination of price and quantity"

ml_anomaly_report.to_csv(
    "ML_Anomaly_Report.csv",
    index=False
)

print("\nML anomaly report saved successfully!")
print("File: ML_Anomaly_Report.csv")