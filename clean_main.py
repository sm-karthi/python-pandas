"""
(a) drop_duplicates() with no arguments compare all columns. If two rows
are the same first one is removed.

(b) To remove duplicates based only on order_id:
    df.drop_duplicates(subset=["order_id"])

(c) For this dataset using drop_duplicates() with no arguments is correct
because the same order_id have multiple products. Only same columns data rows should be removed.
"""

import pandas as pd

def Load_data(path):
    """Load the CSV file."""
    return pd.read_csv(path)

def clean_data(df):
    """Clean the raw data."""

    # WHY: Exact duplicate rows add the same transaction twice.
    df = df.drop_duplicates(keep="first")

    # WHY: Some cells have a empty value so pandas read the column as NaN
    df["city"] = df["city"].fillna("Unknown")

    # Why: Some values in full caps and have a extra spaces so clean this
    df["city"] = df["city"].str.strip().str.replace(r'\s+', ' ', regex=True).str.capitalize()

    # Why: Some values in full caps and have a extra spaces so clean this
    df["product"] = df["product"].str.strip().str.replace(r'\s+', ' ', regex=True).str.capitalize()

    # WHY: some values have an "Rs." prefix so pandas read the column as strings; math is impossible until it's numeric
    df["unit_price"] = pd.to_numeric(df["unit_price"].str.removeprefix("Rs."))

    # WHY: Missing quantities make unknown values, not zero items.
    # Keeping them as NaN avoids creating fake ₹0 orders.    
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')

    # WHY: Missing payment methods should still have a readable value.
    df["payment_mode"] = df["payment_mode"].fillna("Unknown")

    # WHY: Different date formats must become one datetime format
    df["order_date"] = pd.to_datetime(df["order_date"], format="mixed", errors="coerce")

    # .dt.strftime() changes datetime into text.
    # Keep order_date as datetime until saving the CSV.
    # The monthly counts were still correct because the dates were converted

    return df

def validate_data(df):
    """Remove impossible values."""

    # WHY: Negative quantities cannot exist in a completed sales record.
    df = df[df["quantity"] >= 0]

    # WHY: Quantities greater than 100 are considered invalid
    df = df[df["quantity"] <= 100]

    # WHY: Products cannot have zero or negative selling prices.
    df = df[df["unit_price"] >= 0]

    return df

def analyze(df):
    """Print the Part C answers."""

    df["total_amount"] = df["quantity"] * df["unit_price"]

    city_sales = df.groupby("city")["total_amount"].sum()

    print("City with the highest total sales:")
    print(city_sales.idxmax())

    print("Highest total sales:")
    print(city_sales.max())
    
    print("Revenue per product")
    print(df.groupby("product")["total_amount"].sum())

    print("\nOrders per month")
    # order_date is still datetime here.
    print(df.groupby(df["order_date"].dt.month_name())["order_id"].count())

def save_data(df, path):
    """Save cleaned data."""

    # WHY: Format the date only before saving the CSV.
    df["order_date"] = df["order_date"].dt.strftime("%d-%m-%Y")
    df.to_csv(path, index=False)

def main():
    df = Load_data("sales_data_raw.csv")

    print(df.shape)
    print(df.dtypes)
    print(df.isna().sum())

    df = clean_data(df)

    df = validate_data(df)

    analyze(df)

    save_data(df, "sales_data_clean.csv")

    print("Cleaned data saved successfully.")


if __name__ == "__main__":
    main()
