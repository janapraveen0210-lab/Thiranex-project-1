import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("Sample - Superstore.csv", encoding="latin1")

# Convert Order Date to datetime
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Monthly Revenue
monthly_revenue = (
    df.groupby(df["Order Date"].dt.to_period("M"))["Sales"]
    .sum()
)

# Convert index to string for plotting
monthly_revenue.index = monthly_revenue.index.astype(str)

# Plot
plt.figure(figsize=(12,6))
monthly_revenue.plot(kind="line", marker="o")

plt.title("Monthly Sales Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue ($)")
plt.grid(True)

plt.tight_layout()
plt.show()