# Quantum Rebate Optimization: PBM Tradeoff Modeling

This notebook implements a quantum-inspired optimization model to evaluate pharmaceutical rebate strategies under real-world market pressures. The example uses a Binary Quadratic Model (BQM) to assess the tradeoff between rebate generosity and the risk of triggering follow-on demands from competing Pharmacy Benefit Managers (PBMs).

## 🔍 Problem Statement

A large PBM is demanding a 10-point rebate increase to retain formulary status for a specialty drug. Other PBMs (representing 27% of market share) are likely to demand similar concessions if the offer is too generous. The goal is to identify the rebate percentage that minimizes **total financial impact**, considering both:

- Direct revenue loss from the rebate  
- Indirect exposure to spillover effects from other PBMs

## 🎯 Objective Function

Let:

- \( r_i \in \{0, 1\} \): a binary variable for rebate level \( i \) from 1% to 10%  
- \( T_i \): the **total financial impact** for rebate \( i \) (base loss + spillover risk)  
- \( P \): the penalty weight for enforcing one-hot selection (set to 10,000 in the code)  

Then the **objective function** being minimized is:

\[
\text{Minimize: } \sum_{i=1}^{10} T_i \cdot r_i + P \cdot \left( \sum_{i=1}^{10} r_i - 1 \right)^2
\]

**Breaking it down:**

- \( \sum T_i \cdot r_i \): the actual **total impact** we want to minimize  
- \( \left( \sum r_i - 1 \right)^2 \): the **one-hot constraint** — only one rebate can be selected  
- \( P \): a large penalty ensuring the constraint is enforced  

## 🧠 In Practice (from code)

Each \( T_i \) is computed as:

\[
T_i = \text{base\_loss}[i] + \text{follow\_on\_cost}(i)
\]

Only for \( i \geq 9 \), the follow-on cost is non-zero.

The quadratic penalty term expands into:

\[
P \cdot \left( \sum r_i^2 + 2 \sum_{i < j} r_i r_j - 2 \sum r_i + 1 \right)
\]

Since \( r_i^2 = r_i \) for binary variables:

\[
P \cdot \left( - \sum r_i + 2 \sum_{i < j} r_i r_j + 1 \right)
\]

This is reflected in the code:

```python
linear[variables[i]] += P            # Adds penalty to each binary variable
quadratic[(r_i, r_j)] = 2 * P        # Enforces exclusivity across pairs
offset = -2 * P + P                  # Normalizes constant terms
