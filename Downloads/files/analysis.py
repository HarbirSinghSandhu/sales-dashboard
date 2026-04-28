import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# ─── 1. Generate Realistic Sample Dataset ─────────────────────────────────────

np.random.seed(42)

n = 1000
categories   = ["Electronics", "Clothing", "Books", "Home & Kitchen", "Sports"]
regions      = ["North", "South", "East", "West"]
months       = pd.date_range(start="2023-01-01", periods=12, freq="MS")

data = {
    "order_id"    : range(1001, 1001 + n),
    "date"        : np.random.choice(pd.date_range("2023-01-01", "2023-12-31"), n),
    "category"    : np.random.choice(categories, n, p=[0.3, 0.25, 0.15, 0.2, 0.1]),
    "region"      : np.random.choice(regions, n),
    "quantity"    : np.random.randint(1, 10, n),
    "unit_price"  : np.round(np.random.uniform(10, 500, n), 2),
    "discount_pct": np.random.choice([0, 5, 10, 15, 20], n, p=[0.4, 0.2, 0.2, 0.1, 0.1]),
    "customer_age": np.random.randint(18, 70, n),
    "returned"    : np.random.choice([0, 1], n, p=[0.9, 0.1]),
}

df = pd.DataFrame(data)
df["date"]         = pd.to_datetime(df["date"])
df["revenue"]      = np.round(df["quantity"] * df["unit_price"] * (1 - df["discount_pct"] / 100), 2)
df["month"]        = df["date"].dt.to_period("M")
df["month_name"]   = df["date"].dt.strftime("%b")
df["month_num"]    = df["date"].dt.month

# Save dataset
df.to_csv("sales_data.csv", index=False)
print("✅ Dataset created: sales_data.csv")
print(f"   Shape: {df.shape[0]} rows × {df.shape[1]} columns\n")


# ─── 2. Data Cleaning & Overview ──────────────────────────────────────────────

print("=" * 50)
print("  DATA OVERVIEW")
print("=" * 50)
print(f"\nTotal Orders   : {len(df):,}")
print(f"Total Revenue  : ${df['revenue'].sum():,.2f}")
print(f"Avg Order Value: ${df['revenue'].mean():,.2f}")
print(f"Date Range     : {df['date'].min().date()} → {df['date'].max().date()}")
print(f"Missing Values : {df.isnull().sum().sum()}")
print(f"Return Rate    : {df['returned'].mean()*100:.1f}%")


# ─── 3. Key Business Insights ─────────────────────────────────────────────────

print("\n" + "=" * 50)
print("  KEY BUSINESS INSIGHTS")
print("=" * 50)

# Top category by revenue
top_cat = df.groupby("category")["revenue"].sum().idxmax()
top_cat_rev = df.groupby("category")["revenue"].sum().max()
print(f"\n🏆 Best Selling Category : {top_cat} (${top_cat_rev:,.2f})")

# Top region
top_region = df.groupby("region")["revenue"].sum().idxmax()
top_region_rev = df.groupby("region")["revenue"].sum().max()
print(f"📍 Top Region            : {top_region} (${top_region_rev:,.2f})")

# Best month
monthly = df.groupby("month_num")["revenue"].sum()
best_month_num = monthly.idxmax()
best_month_name = pd.Timestamp(2023, best_month_num, 1).strftime("%B")
print(f"📅 Best Month            : {best_month_name} (${monthly.max():,.2f})")

# Highest discount impact
avg_rev_no_disc = df[df["discount_pct"] == 0]["revenue"].mean()
avg_rev_disc    = df[df["discount_pct"] > 0]["revenue"].mean()
print(f"💸 Avg Revenue (no discount)  : ${avg_rev_no_disc:,.2f}")
print(f"💸 Avg Revenue (with discount): ${avg_rev_disc:,.2f}")


# ─── 4. Visualizations ────────────────────────────────────────────────────────

plt.style.use("seaborn-v0_8-whitegrid")
fig = plt.figure(figsize=(18, 14))
fig.suptitle("E-Commerce Sales Dashboard — 2023", fontsize=20, fontweight="bold", y=0.98)

colors = ["#2563EB", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"]

# ── Chart 1: Monthly Revenue Trend ──
ax1 = fig.add_subplot(3, 3, 1)
monthly_rev = df.groupby("month_num")["revenue"].sum()
month_labels = [pd.Timestamp(2023, m, 1).strftime("%b") for m in monthly_rev.index]
ax1.plot(month_labels, monthly_rev.values, color="#2563EB", linewidth=2.5, marker="o", markersize=6)
ax1.fill_between(range(len(month_labels)), monthly_rev.values, alpha=0.15, color="#2563EB")
ax1.set_title("Monthly Revenue Trend", fontweight="bold")
ax1.set_xlabel("Month")
ax1.set_ylabel("Revenue ($)")
ax1.tick_params(axis="x", rotation=45)

# ── Chart 2: Revenue by Category ──
ax2 = fig.add_subplot(3, 3, 2)
cat_rev = df.groupby("category")["revenue"].sum().sort_values(ascending=True)
bars = ax2.barh(cat_rev.index, cat_rev.values, color=colors)
ax2.set_title("Revenue by Category", fontweight="bold")
ax2.set_xlabel("Revenue ($)")
for bar, val in zip(bars, cat_rev.values):
    ax2.text(val + 500, bar.get_y() + bar.get_height()/2,
             f"${val:,.0f}", va="center", fontsize=9)

# ── Chart 3: Revenue by Region (Pie) ──
ax3 = fig.add_subplot(3, 3, 3)
region_rev = df.groupby("region")["revenue"].sum()
ax3.pie(region_rev.values, labels=region_rev.index, autopct="%1.1f%%",
        colors=colors, startangle=90, pctdistance=0.8)
ax3.set_title("Revenue by Region", fontweight="bold")

# ── Chart 4: Orders by Category ──
ax4 = fig.add_subplot(3, 3, 4)
cat_orders = df["category"].value_counts()
ax4.bar(cat_orders.index, cat_orders.values, color=colors)
ax4.set_title("Orders by Category", fontweight="bold")
ax4.set_xlabel("Category")
ax4.set_ylabel("Number of Orders")
ax4.tick_params(axis="x", rotation=15)

# ── Chart 5: Discount vs Revenue ──
ax5 = fig.add_subplot(3, 3, 5)
disc_rev = df.groupby("discount_pct")["revenue"].mean()
ax5.bar(disc_rev.index.astype(str) + "%", disc_rev.values, color="#F59E0B")
ax5.set_title("Avg Revenue by Discount %", fontweight="bold")
ax5.set_xlabel("Discount %")
ax5.set_ylabel("Avg Revenue ($)")

# ── Chart 6: Revenue Distribution ──
ax6 = fig.add_subplot(3, 3, 6)
ax6.hist(df["revenue"], bins=40, color="#8B5CF6", edgecolor="white", alpha=0.85)
ax6.axvline(df["revenue"].mean(), color="red", linestyle="--", linewidth=1.5, label=f"Mean: ${df['revenue'].mean():.0f}")
ax6.set_title("Revenue Distribution", fontweight="bold")
ax6.set_xlabel("Revenue ($)")
ax6.set_ylabel("Frequency")
ax6.legend()

# ── Chart 7: Monthly Orders Count ──
ax7 = fig.add_subplot(3, 3, 7)
monthly_orders = df.groupby("month_num")["order_id"].count()
ax7.bar(month_labels, monthly_orders.values, color="#10B981", alpha=0.85)
ax7.set_title("Monthly Order Count", fontweight="bold")
ax7.set_xlabel("Month")
ax7.set_ylabel("Orders")
ax7.tick_params(axis="x", rotation=45)

# ── Chart 8: Return Rate by Category ──
ax8 = fig.add_subplot(3, 3, 8)
return_rate = df.groupby("category")["returned"].mean() * 100
return_rate = return_rate.sort_values(ascending=False)
ax8.bar(return_rate.index, return_rate.values, color="#EF4444", alpha=0.85)
ax8.set_title("Return Rate by Category (%)", fontweight="bold")
ax8.set_xlabel("Category")
ax8.set_ylabel("Return Rate (%)")
ax8.tick_params(axis="x", rotation=15)

# ── Chart 9: Customer Age Distribution ──
ax9 = fig.add_subplot(3, 3, 9)
ax9.hist(df["customer_age"], bins=20, color="#2563EB", edgecolor="white", alpha=0.85)
ax9.axvline(df["customer_age"].mean(), color="red", linestyle="--", linewidth=1.5,
            label=f"Mean Age: {df['customer_age'].mean():.0f}")
ax9.set_title("Customer Age Distribution", fontweight="bold")
ax9.set_xlabel("Age")
ax9.set_ylabel("Frequency")
ax9.legend()

plt.tight_layout()
plt.savefig("sales_dashboard.png", dpi=150, bbox_inches="tight")
plt.show()
print("\n✅ Dashboard saved as: sales_dashboard.png")


# ─── 5. Summary Report ────────────────────────────────────────────────────────

print("\n" + "=" * 50)
print("  FULL CATEGORY BREAKDOWN")
print("=" * 50)
summary = df.groupby("category").agg(
    Total_Orders   = ("order_id", "count"),
    Total_Revenue  = ("revenue", "sum"),
    Avg_Order_Value= ("revenue", "mean"),
    Return_Rate_pct= ("returned", lambda x: round(x.mean() * 100, 1))
).sort_values("Total_Revenue", ascending=False)

summary["Total_Revenue"]   = summary["Total_Revenue"].map("${:,.2f}".format)
summary["Avg_Order_Value"] = summary["Avg_Order_Value"].map("${:,.2f}".format)
print(summary.to_string())

print("\n" + "=" * 50)
print("  REGIONAL BREAKDOWN")
print("=" * 50)
region_summary = df.groupby("region").agg(
    Total_Orders  = ("order_id", "count"),
    Total_Revenue = ("revenue", "sum"),
    Avg_Discount  = ("discount_pct", "mean")
).sort_values("Total_Revenue", ascending=False)

region_summary["Total_Revenue"] = region_summary["Total_Revenue"].map("${:,.2f}".format)
region_summary["Avg_Discount"]  = region_summary["Avg_Discount"].map("{:.1f}%".format)
print(region_summary.to_string())

print("\n✅ Analysis complete!")
