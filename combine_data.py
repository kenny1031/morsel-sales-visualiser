import pandas as pd
import os

# Get a list of paths to all csv files
data_dir = "data"
files = [
    os.path.join(data_dir, f)
    for f in os.listdir(data_dir)
    if f.startswith("daily_sales_data_") and f.endswith(".csv")
]

frames = []
for path in files:
    df = pd.read_csv(path)
    new_df = df[df["product"] == "pink morsel"].copy()
    # Convert price column to float type and calculate price
    new_df["price"] = new_df["price"].str.replace("$", "", regex=False).astype(float)
    new_df["sales"] = new_df["price"] * new_df["quantity"]
    frames.append(new_df[['sales', 'date', 'region']])

pd.concat(frames).to_csv("pink_morsel_sales.csv", index=False)
print("✅pink_morsel_sales.csv written")






