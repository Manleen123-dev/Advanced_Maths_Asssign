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
plt.figure()
plt.hist(x, bins=50)
plt.title("Original NO2 Distribution")
plt.xlabel("NO2")
plt.ylabel("Frequency")
plt.savefig(f"{PLOT_FOLDER}/histogram_no2.png")
plt.close()

# Histogram transformed
plt.figure()
plt.hist(z, bins=50, density=True)
plt.title("Transformed Variable z Distribution")
plt.xlabel("z")
plt.ylabel("Density")
plt.savefig(f"{PLOT_FOLDER}/distribution_z.png")
plt.close()

print("Plots saved.")

print("\nProject completed successfully.")
