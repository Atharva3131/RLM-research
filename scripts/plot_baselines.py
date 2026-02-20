import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results.csv")

# Average output length per method
avg_lengths = df.groupby("method")["output_length"].mean()

plt.figure()
avg_lengths.plot(kind="bar")

plt.xlabel("Method")
plt.ylabel("Average Output Length (characters)")
plt.title("Baseline Comparison: Output Length")

plt.xticks(rotation=0)
plt.grid(axis="y")
plt.tight_layout()
plt.savefig("fig_baseline_comparison.png", dpi=300)
plt.show()