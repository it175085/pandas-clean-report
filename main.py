import pandas as pd

from pathlib import Path

# -----------------------------------------
# 1️⃣ ΒΡΙΣΚΟΥΜΕ ΤΑ PATHS
# -
# Παίρνουμε τον φάκελο όπου βρίσκεται το main.py
root = Path(__file__).parent

# Φτιάχνουμε τη διαδρομή για το αρχείο δεδομένων
data_path = root / "data" / "sales.csv"

# Φτιάχνουμε τη διαδρομή για τον φάκελο output
output_path = root / "output"


# Αν ο φάκελος output δεν υπάρχει, τον δημιουργεί
output_path.mkdir(exist_ok=True)

df = pd.read_csv(data_path)
print(df.head().to_string())

# -----------------------------------------
# 3️⃣ ΚΑΘΑΡΙΣΜΟΣ
# -----------------------------------------

# Μετατρέπουμε τη στήλη order_date σε ημερομηνία
df["order_date"] = pd.to_datetime(df["order_date"],errors="coerce")


# Μετατρέπουμε quantity και unit_price σε αριθμούς
df["quantity"] = pd.to_numeric(df["quantity"],errors = "coerce")
df["unit_price"] = pd.to_numeric(df["unit_price"],errors="coerce")

# Αφαιρούμε γραμμές που έχουν κενές τιμές
df.dropna()

# Κρατάμε μόνο θετικές τιμές
df = df[(df["quantity"] > 0) & (df["unit_price"] > 0)]

# -----------------------------------------
# 4️⃣ ΔΗΜΙΟΥΡΓΙΑ ΝΕΑΣ ΣΤΗΛΗΣ
# -----------------------------------------

df["revenue"] = df["quantity"] * df["unit_price"]

# -----------------------------------------
# 5️⃣ ΥΠΟΛΟΓΙΣΜΟΣ KPIs
# -----------------------------------------

total_revenue = df["revenue"].sum()
total_orders = df["order_id"].nunique()
total_customers = df["customer_id"].nunique()

# -----------------------------------------
# 6️⃣ TOP CATEGORIES
# -----------------------------------------
# -----------------------------------------
# 6️⃣ TOP CATEGORIES (καθαρό για Excel)
# -----------------------------------------

top_categories = (
    df.groupby("category", as_index=False)
      .agg(
          total_revenue=("revenue", "sum"),
          total_orders=("order_id", "count"),
      )
      .sort_values("total_revenue", ascending=False)
)

# στρογγυλοποίηση για να φαίνεται ωραίο
top_categories["total_revenue"] = top_categories["total_revenue"].round(2)

# αποθήκευση με κανονικές στήλες (χωρίς index)
top_categories.to_csv(output_path / "top_categories.csv", index=False)
# -----------------------------------------
# 7️⃣ ΑΠΟΘΗΚΕΥΣΗ ΑΡΧΕΙΩΝ
# -----------------------------------------

# Αποθηκεύουμε καθαρισμένο datase
df.to_csv(output_path / "clean_sales.csv",index=False)

# Αποθηκεύουμε top categories
top_categories.to_csv(output_path / "top_categories.csv", index=False)

# -----------------------------------------
# 8️⃣ ΔΗΜΙΟΥΡΓΙΑ REPORT
# -----------------------------------------

report_text = f"""
Sales Report

Total Revenue: {total_revenue:.2f}
Total Orders: {total_orders}
Total Customers: {total_customers}
"""

with open(output_path / "report.txt","w",encoding="utf-8") as f:
    f.write(report_text)

print("\n✅ Ολοκληρώθηκε το report!")