# E-Commerce Sales Data Analysis & Dashboard 📊

An end-to-end Python data analysis project that explores e-commerce sales data, uncovers business insights, and generates a full visual dashboard using **Pandas, NumPy, Matplotlib, and Seaborn**.

---

## 📌 What This Project Does

- ✅ Generates and cleans a realistic e-commerce sales dataset (1,000 orders)
- ✅ Performs full Exploratory Data Analysis (EDA)
- ✅ Extracts key business insights (top category, best region, best month)
- ✅ Builds a 9-chart visual dashboard saved as PNG
- ✅ Produces category and regional breakdown reports

---

## 📊 Dashboard Preview

The script generates a `sales_dashboard.png` with these 9 charts:

| Chart | Insight |
|-------|---------|
| Monthly Revenue Trend | How sales grew month by month |
| Revenue by Category | Which category earns most |
| Revenue by Region | Regional sales share (pie chart) |
| Orders by Category | Most popular product categories |
| Avg Revenue by Discount % | How discounts affect revenue |
| Revenue Distribution | Spread of order values |
| Monthly Order Count | Busiest months for orders |
| Return Rate by Category | Which categories get returned most |
| Customer Age Distribution | Who is buying |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.x | Core language |
| Pandas | Data manipulation & cleaning |
| NumPy | Numerical operations |
| Matplotlib | Charts and dashboard |
| Seaborn | Styling and visual themes |

---

## ⚙️ Setup & Run

1. Clone the repository
```bash
git clone https://github.com/HarbirSinghSandhu/sales-dashboard.git
cd sales-dashboard
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the analysis
```bash
python analysis.py
```

4. Output
- `sales_data.csv` — generated dataset
- `sales_dashboard.png` — full 9-chart dashboard
- Printed insights and summary tables in terminal

---

Project Structure

```
sales-dashboard/
│
├── analysis.py        # Main analysis script
├── requirements.txt   # Python dependencies
├── sales_data.csv     # Auto-generated dataset (after running)
├── sales_dashboard.png# Auto-generated dashboard (after running)
└── README.md          # Project documentation
```

---

Key Insights Found

- **Electronics** is the top revenue-generating category
- **Discounts of 10–15%** generate higher average order values
- **Q3 (Jul–Sep)** shows the strongest sales performance
- **Return rate** is highest in Electronics (~11%)
- **Average customer age** is 43 years

---

## 🚀 Skills Demonstrated

- Data cleaning and preprocessing with Pandas
- Exploratory Data Analysis (EDA)
- Statistical summarization (groupby, aggregation)
- Multi-chart dashboard creation with Matplotlib
- Business insight extraction from raw data

---

## 👨‍💻 Author

**Harbir Singh Sandhu**

