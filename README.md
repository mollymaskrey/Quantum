# 💊 Quantum Rebate Optimization

This project demonstrates how to formulate a real-world pharmacy rebate negotiation problem as a Quadratic Unconstrained Binary Optimization (QUBO) model. It's built using the D-Wave Ocean SDK and is designed for execution on a simulated annealer or quantum processing unit (QPU).

---

## 🎯 Objective

A Pharmacy Benefit Manager (PBM) offers 10 potential rebate levels, from 1% to 10%. The manufacturer must select one — and only one — level that minimizes total projected loss, which includes both base discounting and any anticipated market spillover risk from competitors.

The goal: **select exactly one rebate level** that minimizes the following total cost.

### 🔻 Objective Function

Let:

- \( r_i \in \{0, 1\} \): a binary decision variable (1 if rebate level _i_ is chosen, 0 otherwise)
- \( T_i \): total financial impact (base loss + spillover risk) of rebate level _i_
- \( P \): penalty weight to enforce one-hot encoding (only one rebate can be selected)

Then the function being minimized is:

\[
\text{Minimize: } \sum_{i=1}^{10} T_i \cdot r_i + P \cdot \left( \sum_{i=1}^{10} r_i - 1 \right)^2
\]

---

## 🧠 Interpreting the Model

- \( \sum T_i \cdot r_i \): the total projected financial loss for the selected rebate
- \( \left( \sum r_i - 1 \right)^2 \): a one-hot constraint to ensure exactly one rebate level is chosen
- \( P \): a large penalty (10,000) used to strictly enforce the constraint

---

## 🔢 QUBO Expansion

The squared penalty expands into pairwise interactions:

\[
P \cdot \left( - \sum r_i + 2 \sum_{i<j} r_i r_j + 1 \right)
\]

This results in:

- Linear coefficients (penalties): \( P \cdot r_i \)
- Quadratic coefficients (cross-terms): \( 2P \cdot r_i r_j \)
- Constant offset: \( -2P + P = -P \)

---

## 📦 Requirements

- Python 3.8+
- D-Wave Ocean SDK  
  ```bash
  pip install dwave-ocean-sdk
