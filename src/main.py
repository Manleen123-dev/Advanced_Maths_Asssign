import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import os

# ==============================
# CONFIG
# ==============================

DATA_PATH = "../data/data.csv"
OUTPUT_FOLDER = "../output"
PLOT_FOLDER = "../plots"

ROLL_NUMBER = 102303599

# create folders if not exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(PLOT_FOLDER, exist_ok=True)

# ==============================
# LOAD DATA
# ==============================

print("Loading dataset...")

data = pd.read_csv(DATA_PATH, encoding="latin1")

x = data["no2"].dropna().values

print(f"Total samples: {len(x)}")

# ==============================
# COMPUTE CONSTANTS
# ==============================

a_r = 0.05 * (ROLL_NUMBER % 7)
b_r = 0.3 * ((ROLL_NUMBER % 5) + 1)

print(f"a_r: {a_r}")
print(f"b_r: {b_r}")

# ==============================
# TRANSFORM DATA
# ==============================

z = x + a_r * np.sin(b_r * x)

# ==============================
# LEARN PARAMETERS
# ==============================

mu = np.mean(z)

variance = np.var(z)

lam = 1 / (2 * variance)

c = 1 / np.sqrt(2 * np.pi * variance)

print("\nLearned Parameters:")
print(f"mu: {mu}")
print(f"lambda: {lam}")
print(f"c: {c}")

# ==============================
# SAVE PARAMETERS
# ==============================

# JSON
params = {
    "mu": float(mu),
    "lambda": float(lam),
    "c": float(c)
}

with open(f"{OUTPUT_FOLDER}/parameters.json", "w") as f:
    json.dump(params, f, indent=4)

# TXT
with open(f"{OUTPUT_FOLDER}/parameters.txt", "w") as f:
    f.write(f"mu = {mu}\n")
    f.write(f"lambda = {lam}\n")
    f.write(f"c = {c}\n")

# CSV summary
summary = pd.DataFrame({
    "Parameter": ["mu", "lambda", "c"],
    "Value": [mu, lam, c]
})

summary.to_csv(f"{OUTPUT_FOLDER}/summary.csv", index=False)

print("Parameters saved.")

# ==============================
# SAVE GRAPHS
# ==============================

# Histogram original


# Create smooth x range centered around mean
x_vals = np.linspace(mu - 4*np.sqrt(variance), mu + 4*np.sqrt(variance), 500)

# Gaussian PDF formula
pdf_vals = c * np.exp(-lam * (x_vals - mu)**2)

# Plot histogram (density normalized)
plt.figure(figsize=(10,6))

plt.hist(z,
         bins=100,
         density=True,
         alpha=0.6,
         label="Transformed Data Histogram")

# Plot bell curve
plt.plot(x_vals,
         pdf_vals,
         linewidth=3,
         label="Learned Gaussian PDF (Bell Curve)")

plt.title("Bell-Shaped Gaussian Curve Fit on Transformed Data")
plt.xlabel("z")
plt.ylabel("Probability Density")
plt.legend()

plt.savefig("../plots/bell_curve_fit.png", dpi=300)
plt.show()
