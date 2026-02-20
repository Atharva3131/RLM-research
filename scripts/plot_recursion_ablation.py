import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("recursion_ablation.csv")

plt.figure()
plt.plot(
    df["max_recursion_depth"],
    df["output_length"],
    marker="o"
)

plt.xlabel("Maximum Recursion Depth")
plt.ylabel("Output Length (characters)")
plt.title("Effect of Recursion Depth on Output Length")

plt.grid(True)
plt.tight_layout()
plt.savefig("fig_recursion_ablation.png", dpi=300)
plt.show()