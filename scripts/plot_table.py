import pandas as pd

df = pd.read_csv("results.csv")

summary = df.groupby("method").agg({
    "num_llm_calls": "mean",
    "output_length": "mean",
    "success": "mean"
}).reset_index()

print(summary)