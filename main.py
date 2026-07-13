import pandas as pd

# Load the CSV into a DataFrame
df = pd.read_csv("sales_data_raw.csv")

# =========================
# Part 1
# =========================

# Question 1: Load the CSV into a DataFrame.
print(df)

# Question 2: Report number of rows, number of columns, and the dtype of each column.
print(df.shape)
print(df.dtypes)

# Question 3: Which columns have missing values, and how many in each?
print(df.isna().sum())


# =========================
# Part 2
# =========================

# Question 1: Remove exact duplicate rows. How many did you remove?

duplicate_rows = df[df.duplicated(keep="first")]

print(f"Number of duplicate rows: {len(duplicate_rows)}")

print("Rows that will be removed:")
print(duplicate_rows)

df = df.drop_duplicates(keep="first")

print("Shape after removing duplicates:", df.shape)


# Question 2: Fix the city column.

df["city"] = df["city"].str.strip().str.replace(r'\s+', ' ', regex=True).str.capitalize()

print(df["city"])


# Question 3: Fix the product column casing the same way.

df["product"] = df["product"].str.strip().str.replace(r'\s+', ' ', regex=True).str.capitalize()

print(df["product"])


# Question 4: Convert unit_price to numeric.

print(df.dtypes)

df["unit_price"] = pd.to_numeric(df["unit_price"].str.removeprefix("Rs."))

print(df.dtypes)


# Question 5: Convert quantity to numeric.

df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)

print(df["quantity"])


# Question 6: Convert order_date to datetime.

df["order_date"] = pd.to_datetime(
    df["order_date"],
    format="mixed",
    errors="coerce"
).dt.strftime("%d-%m-%Y")

print(df["order_date"])


# Question 7: Find impossible values.

df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

limit = 100

impossible_vals = df[
    (df["quantity"] < 0) |
    (df["quantity"] > limit) |
    (df["unit_price"] <= 0)
]

print(impossible_vals)


# Question 8: Fill missing payment_mode.

df["payment_mode"] = df["payment_mode"].fillna("Unknown")

print(df["payment_mode"])


# =========================
# Part 3
# =========================

# Question 1: Add a total_amount column = quantity × unit_price.

df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)

df["unit_price"] = pd.to_numeric(df["unit_price"].astype(str).str.removeprefix("Rs."), errors="coerce")

df["total_amount"] = df["quantity"] * df["unit_price"]

print(df)


# Question 2: Which city has the highest total sales?

df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)

df["unit_price"] = pd.to_numeric(df["unit_price"].astype(str).str.removeprefix("Rs."), errors="coerce")

df["total_amount"] = df["quantity"] * df["unit_price"]

city_sales = df.groupby("city")["total_amount"].sum()

print("City with the highest total sales:")
print(city_sales.idxmax())

print("Highest total sales:")
print(city_sales.max())


# Question 3: What is the total revenue per product?

df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)

df["unit_price"] = pd.to_numeric(df["unit_price"].astype(str).str.removeprefix("Rs."), errors="coerce")

df["total_amount"] = df["quantity"] * df["unit_price"]

product_revenue = df.groupby("product")["total_amount"].sum()

print("Total revenue per product:")
print(product_revenue)


# Question 4: Number of orders placed in each month.

df["order_date"] = pd.to_datetime(df["order_date"], format="mixed", errors="coerce")

monthly_orders = df.groupby(df["order_date"].dt.month_name())["order_id"].count()

print("Number of orders placed in each month:")
print(monthly_orders)


# Question 5: Save the cleaned data to sales_data_clean.csv (without the index column).

df = df.drop_duplicates(keep="first")

df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)

df["unit_price"] = pd.to_numeric(df["unit_price"].astype(str).str.removeprefix("Rs."), errors="coerce")

df["city"] = df["city"].fillna("Unknown")
df["city"] = df["city"].str.strip().str.replace(r"\s+", " ", regex=True).str.capitalize()

df["product"] = df["product"].str.strip().str.replace(r"\s+", " ", regex=True).str.capitalize()

df["order_date"] = pd.to_datetime(df["order_date"], format="mixed", errors="coerce").dt.strftime("%d-%m-%Y")

df["payment_mode"] = df["payment_mode"].fillna("Unknown")

df.to_csv("sales_data_clean.csv", index=False)

print("Cleaned data has been saved to 'sales_data_clean.csv'.")
