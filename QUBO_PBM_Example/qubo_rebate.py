#!/usr/bin/env python
# coding: utf-8

# # QUBO Analysis of simulated rebate negotiation

# In[38]:


import dimod
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# ---------------------------------------
# Problem Context:
#
# PBM_A demands a 10-point rebate increase to keep DRUG_X in formulary.
# PBM_B (12% of volume) and PBM_C (15%) are observing closely and may also demand better terms
# if PBM_A receives a generous deal.
#
# Objective: Choose the rebate % that minimizes the *total impact*:
# = base revenue risk + exposure to follow-on rebate demands (if too generous)
# ---------------------------------------

# Wholesale Acquisition Cost (WAC) per unit
WAC = 525.00

# PBM market shares
pbm_b_share = 0.12
pbm_c_share = 0.15

# Base financial impact at each rebate level (estimated revenue loss in $M)
base_loss = {
    1: 4.3, 2: 4.0, 3: 3.6, 4: 3.3, 5: 3.2,
    6: 2.5, 7: 2.2, 8: 2.0, 9: 1.7, 10: 1.5
}

# Function to compute follow-on cost from other PBMs
def follow_on_cost(rebate):
    if rebate >= 9:
        # Higher chance of triggering rebate demands from PBM_B and PBM_C
        total_cartons = 100000  # Assumed annual volume
        est_rebate_increase = 0.03  # estimated 3% extra rebate if triggered
        return (pbm_b_share + pbm_c_share) * total_cartons * WAC * est_rebate_increase / 1e6
    return 0.0

# Total impact = base loss + follow-on risk
rebate_levels = list(range(1, 11))
total_impact = {r: base_loss[r] + follow_on_cost(r) for r in rebate_levels}

# Variables and BQM setup
variables = [f"r{i}" for i in rebate_levels]
linear = {f"r{i}": total_impact[i] for i in rebate_levels}
P = 10000  # One-hot constraint penalty
quadratic = {}
for i in range(len(variables)):
    linear[variables[i]] += P
    for j in range(i + 1, len(variables)):
        quadratic[(variables[i], variables[j])] = 2 * P
offset = -2 * P + P

# Solve using ExactSolver
bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, dimod.BINARY)
sampler = dimod.ExactSolver()
response = sampler.sample(bqm)

# Extract valid samples (only one rebate level selected)
valid_samples = []
for sample, energy in zip(response.samples(), response.data_vectors['energy']):
    active = [var for var, val in sample.items() if val == 1 and var.startswith("r")]
    if len(active) == 1:
        rebate = int(active[0][1:])
        valid_samples.append({"Rebate_Offered_%": rebate, "Total_Impact_M": energy})

df = pd.DataFrame(valid_samples).sort_values("Total_Impact_M").reset_index(drop=True)

# Best result
best = df.iloc[0]
rebate = best['Rebate_Offered_%']
impact = best['Total_Impact_M']

# Executive Summary Output
print("\n Executive Summary:")
print(
    f"PBM_A is requesting a 10-point rebate increase to retain formulary access for DRUG_X. "
    f"However, an overly generous offer may trigger similar demands from PBM_B and PBM_C, "
    f"which together represent over 25% of prescription volume.\n\n"
    f"This optimization model evaluated each rebate level from 1% to 10%, weighing direct financial loss "
    f"against follow-on risk from other PBMs.\n\n"
    f"The optimal offer is: **{rebate}% rebate**, with a projected annual impact of "
    f"**${impact:.2f}M**.\n\n"
    f"This middle-ground offer may secure access with PBM_A while minimizing broader exposure."
)

# Top 5 strategies
print("\nTop Rebate Strategies by Estimated Total Impact:")
print(df[['Rebate_Offered_%', 'Total_Impact_M']].head(5))

# Plot
plt.figure(figsize=(12, 6))
sns.set_style("whitegrid")

bars = plt.bar(df['Rebate_Offered_%'], df['Total_Impact_M'], color='skyblue', edgecolor='black')

# Highlight best bar
min_impact = df['Total_Impact_M'].min()
min_idx = df['Total_Impact_M'].idxmin()
best_rebate = df.loc[min_idx, 'Rebate_Offered_%']
bars[min_idx].set_color('green')

plt.text(
    x=best_rebate,
    y=min_impact + 0.5,
    s=f"Best: {best_rebate}%\n${min_impact:.2f}M",
    ha='center',
    va='bottom',
    fontsize=10,
    fontweight='bold',
    color='darkgreen'
)

plt.xlabel("Rebate Increase Offered (%)", fontsize=12)
plt.ylabel("Total Revenue Impact (Millions USD)", fontsize=12)
plt.title("Quantum-Optimized Rebate Strategy\n(Including Spillover Risk from PBM_B and PBM_C)", fontsize=14)
plt.xticks(df['Rebate_Offered_%'])
plt.tight_layout()
plt.show()


# In[ ]:




