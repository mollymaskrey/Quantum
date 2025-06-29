# Quantum Rebate Optimization: PBM Tradeoff Modeling

This notebook implements a quantum-inspired optimization model to evaluate pharmaceutical rebate strategies under real-world market pressures. The example uses a Binary Quadratic Model (BQM) to assess the tradeoff between rebate generosity and the risk of triggering follow-on demands from competing Pharmacy Benefit Managers (PBMs).

## 🔍 Problem Statement

A large PBM is demanding a 10-point rebate increase to retain formulary status for a specialty drug. Other PBMs (representing 27% of market share) are likely to demand similar concessions if the offer is too generous. The goal is to identify the rebate percentage that minimizes **total financial impact**, considering both:

- Direct revenue loss from the rebate  
- Indirect exposure to spillover effects from other PBMs

## 🎯 Objective Function

Let:

- `r_i ∈ {0, 1}`: a binary variable for rebate level `i` from 1% to 10%  
- `T_i`: the **total financial impact** for rebate `i` (base loss + spillover risk)  
- `P`: the penalty weight for enforcing one-hot selection (set to 10,000 in the code)  

Then the **objective function** being minimized is:

```
Minimize:  ∑ T_i * r_i  +  P * (∑ r_i - 1)²
```

**Breaking it down:**

- `∑ T_i * r_i`: the actual **total impact** we want to minimize  
- `(∑ r_i - 1)²`: the **one-hot constraint** — only one rebate can be selected  
- `P`: a large penalty ensuring the constraint is enforced  

## 🧠 In Practice (from code)

Each `T_i` is computed as:

```
T_i = base_loss[i] + follow_on_cost(i)
```

Only for `i >= 9`, the follow-on cost is non-zero.

The quadratic penalty term expands into:

```
P * ( ∑ r_i² + 2 ∑ r_i r_j - 2 ∑ r_i + 1 )
```

Since `r_i² = r_i` for binary variables:

```
P * ( - ∑ r_i + 2 ∑ r_i r_j + 1 )
```

This is reflected in the code:

```python
linear[variables[i]] += P             # Adds penalty to each binary variable
quadratic[(r_i, r_j)] = 2 * P         # Enforces exclusivity across pairs
offset = -2 * P + P                   # Normalizes constant terms
```

## 🧪 Example Use Case

This notebook can be used to evaluate whether offering a high rebate (e.g., 10%) is worth the risk of triggering follow-on demands from other PBMs. The cost model captures both direct and indirect financial consequences, and the QUBO formulation enables the problem to be solved using D-Wave’s quantum annealing methods or classical solvers.

## 🗂️ Repo Structure

```
QUBO_PBM_Example/
├── pbm_qubo_model.ipynb        # Jupyter Notebook implementing the QUBO
├── README.md                   # This file
├── data/
│   └── base_losses.csv         # Simulated input data
└── output/
    └── best_solution.json      # Sample solution output
```

## 🛠️ Requirements

- Python 3.8+
- `dimod`, `dwave-ocean-sdk`, or equivalent libraries
- Jupyter (optional for notebook use)

## 📄 License

MIT License. Use at your own risk. Not affiliated with any actual PBM or pharma entity.
