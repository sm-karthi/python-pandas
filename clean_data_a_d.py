import pandas as pd

def load_data():
    """Load CSV files."""
    customers_df = pd.read_csv("customers.csv")
    orders_df = pd.read_csv("orders.csv")
    return customers_df, orders_df

def clean_orders(orders_df):
    """Clean orders customer_id."""
    orders_df["customer_id"] = orders_df["customer_id"].str.upper()
    orders_df["customer_id"] = orders_df["customer_id"].fillna("Unknown")
    orders_df["customer_id"] = orders_df["customer_id"].str.strip().str.replace(r"\s+", "", regex=True)
    return orders_df

def clean_customers(customers_df):
    """Remove duplicate customer IDs."""

    customers_df = customers_df.drop_duplicates(subset="customer_id", keep="first")

    return customers_df

def merge_data(customers_df, orders_df):
    """Merge customers and orders."""

    merged_df = pd.merge(
        orders_df,
        customers_df,
        on="customer_id",
        how="left",
        validate="many_to_one"
    )

    merged_df["revenue"] = merged_df["quantity"] * merged_df["unit_price"]

    return merged_df

def check_duplicate_customer_id(df):
    """Check whether customer_id contains duplicates."""

    duplicate_rows = df[df.duplicated(subset="customer_id")]

    if len(duplicate_rows) > 0:
        print("No, customer_id column have duplicates")
        print("Duplicate rows")
        print(duplicate_rows)
    else:
        print("Yes, customer_id column have no duplicates.")

def check_orders_customer_id(df):
    """Check problems in the customer_id column."""

    # Check empty values count
    print("Empty values")
    print(df["customer_id"].isna().sum())

    # Check duplicate
    duplicate_rows = df[df.duplicated(subset="customer_id")]
    print("Duplicate rows")
    print(duplicate_rows)

    # Check lower case count
    lowercase_count = df["customer_id"].apply(
        lambda x: sum(1 for char in str(x) if char.islower())
    ).tail()

    print("Lower case count")
    print(lowercase_count)

    # Check upper case count
    uppercase_count = df["customer_id"].apply(
        lambda x: sum(1 for char in str(x) if char.isupper())
    ).tail()

    print("Upper case count")
    print(uppercase_count)

    # Check extra spaces values
    selected_row = (
        df["customer_id"].str.contains(r"\s+", regex=True, na=False) |
        (df["customer_id"] != df["customer_id"].str.strip())
    )

    print("Count:", selected_row.sum())

    print("Values with extra spaces:")
    print(df.loc[selected_row, "customer_id"])

# Part A 
# Question 1 
def part_a_question1():
    customers_df, orders_df = load_data()

    print("Customers dataframe")
    print(customers_df.shape)
    print(customers_df.dtypes)

    print("Orders dataframe")
    print(orders_df.shape)
    print(orders_df.dtypes)

def part_a_question2():
    customers_df, orders_df = load_data()

    check_orders_customer_id(orders_df)

# Question 3 
def part_a_question3():
    customers_df, orders_df = load_data()

    check_duplicate_customer_id(customers_df)

# Part B 
# Question 1 
def part_b_question1():
    customers_df, orders_df = load_data()

    orders_df = clean_orders(orders_df)

    print(orders_df["customer_id"])

# Question 2 
def part_b_question2():
    customers_df, orders_df = load_data()

    customers_df = clean_customers(customers_df)
    orders_df = clean_orders(orders_df)

    merged_df = pd.merge(orders_df, customers_df, on="customer_id", how="inner")

    merged_df["revenue"] = merged_df["quantity"] * merged_df["unit_price"]

    print(merged_df)

# Part C 
# Question 1 
def part_c_question1():
    customers_df, orders_df = load_data()

    customers_df = clean_customers(customers_df)
    orders_df = clean_orders(orders_df)

    merged_df = merge_data(customers_df, orders_df)

    merged_df.to_csv("merged_cus_ord_left.csv", index=False)

# Question 2 
def part_c_question2():
    customers_df, orders_df = load_data()

    customers_df = clean_customers(customers_df)
    orders_df = clean_orders(orders_df)

    merged_df = pd.merge(
        orders_df,
        customers_df,
        on="customer_id",
        how="left",
        indicator=True
    )

    merged_df["revenue"] = merged_df["quantity"] * merged_df["unit_price"]

    failed_matches = merged_df[merged_df["_merge"] == "left_only"]

    print("Count of failed matches:", len(failed_matches))
    print("Order IDs:", failed_matches["order_id"].tolist())

# Question 3 
def part_c_question3():
    customers_df, orders_df = load_data()

    customers_df = clean_customers(customers_df)
    orders_df = clean_orders(orders_df)

    merged_df = pd.merge(
        orders_df,
        customers_df,
        on="customer_id",
        how="left",
        validate="many_to_one"
    )

    merged_df["revenue"] = merged_df["quantity"] * merged_df["unit_price"]

    merged_df.to_csv("merged_cus_ord_validate.csv", index=False)

# Part D 
# Question 1 
def part_d_question1():
    customers_df, orders_df = load_data()

    customers_df = clean_customers(customers_df)
    orders_df = clean_orders(orders_df)

    merged_df = merge_data(customers_df, orders_df)

    city_revenue = merged_df.groupby("city")["revenue"].sum()

    print(city_revenue)

# Question 2 
def part_d_question2():
    customers_df, orders_df = load_data()

    customers_df = clean_customers(customers_df)
    orders_df = clean_orders(orders_df)

    merged_df = merge_data(customers_df, orders_df)

    customer = merged_df.groupby(["customer_id", "customer_name"])["revenue"].sum()

    print("Most spent customer:")
    print(customer.idxmax())

    print("Highest most spent:")
    print(customer.max())

# Question 3 
def part_d_question3():
    customers_df, orders_df = load_data()

    orders_df = clean_orders(orders_df)

    merged_df = pd.merge(orders_df, customers_df, on="customer_id", how="left")

    merged_df["revenue"] = merged_df["quantity"] * merged_df["unit_price"]

    segment_revenue = merged_df.groupby("segment", dropna=False)["revenue"].sum()

    print(segment_revenue)

# Question 4 
def part_d_question4():
    customers_df, orders_df = load_data()

    customers_df = clean_customers(customers_df)
    orders_df = clean_orders(orders_df)

    merged_df = pd.merge(customers_df, orders_df, on="customer_id", how="left")

    no_orders = merged_df[merged_df["order_id"].isna()]

    print(no_orders[["customer_id", "customer_name"]])

def main():
    part_a_question1()
    # part_a_question2()
    # part_a_question3()

    # part_b_question1()
    # part_b_question2()

    # part_c_question1()
    # part_c_question2()
    # part_c_question3()

    # part_d_question1()
    # part_d_question2()
    # part_d_question3()
    # part_d_question4()


if __name__ == "__main__":
    main()
