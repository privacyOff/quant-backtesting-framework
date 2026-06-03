import pandas as pd
import matplotlib.pyplot as plt


data = {
    "Strategy": [
        "SMA Crossover",
        "Momentum",
        "Mean Reversion"
    ],
    "Sharpe Ratio": [
        0.9236687045,
        0.8632979020,
        0.5200533520
    ],
    "CAGR": [
        0.1867005667,
        0.1739724810,
        0.0868159036
    ],
    "Total Return": [
        1.3486631568,
        1.2256677080,
        0.5147797695
    ]
}

df = pd.DataFrame(data)

fig, ax = plt.subplots(figsize=(10, 6))

x = range(len(df))
width = 0.25

ax.bar(
    [i - width for i in x],
    df["Sharpe Ratio"],
    width,
    label="Sharpe"
)

ax.bar(
    x,
    df["CAGR"],
    width,
    label="CAGR"
)

ax.bar(
    [i + width for i in x],
    df["Total Return"],
    width,
    label="Total Return"
)

ax.set_xticks(list(x))
ax.set_xticklabels(df["Strategy"])

ax.set_title("Strategy Comparison")
ax.set_ylabel("Metric Value")
ax.legend()

plt.tight_layout()

plt.savefig(
    "outputs/charts/strategy_comparison.png",
    dpi=300
)

plt.show()