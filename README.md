# Quantum Rebate Optimization: PBM Tradeoff Modeling

This notebook implements a quantum-inspired optimization model to evaluate pharmaceutical rebate strategies under real-world market pressures. The example uses a Binary Quadratic Model (BQM) to assess the tradeoff between rebate generosity and the risk of triggering follow-on demands from competing Pharmacy Benefit Managers (PBMs).

## 🔍 Problem Statement

A large PBM is demanding a 10-point rebate increase to retain formulary status for a specialty drug. Other PBMs (representing 27% of market share) are likely to demand similar concessions if the offer is too generous. The goal is to identify the rebate percentage that minimizes **total financial impact**, considering both:

- Direct revenue loss from the rebate
- Indirect exposure to spillover effects from other PBMs

## 🎯 Objective Function

Let:

- `rᵢ ∈ {0, 1}` be a binary variable for rebate level *i* from 1% to 10%
- `Tᵢ` be the **total financial impact** for rebate *i* (base loss + spillover risk)
- `P` be the penalty weight for enforcing one-hot selection (set to 10,000 in the code)

The objective function being minimized is:

```
Minimize:  ∑(Tᵢ · rᵢ)  +  P · ( ∑(rᵢ) - 1 )²
```

### Breakdown

- `∑ Tᵢ · rᵢ`: actual financial cost (loss + risk)
- `( ∑ rᵢ - 1 )²`: enforces one and only one rebate level is selected
- `P`: large penalty to make the constraint hard (10,000)

## 🧠 In Practice (from code)

Each `Tᵢ` is calculated as:

```
Tᵢ = base_loss[i] + follow_on_cost(i)
```

Where `follow_on_cost(i)` is only non-zero when `i ≥ 9`.

The quadratic penalty term expands as:

```
P · ( ∑ rᵢ² + 2∑₍ᵢ<ⱼ₎ rᵢ·rⱼ - 2∑ rᵢ + 1 )
```

Since `rᵢ² = rᵢ` for binary variables, this simplifies to:

```
P · ( -∑ rᵢ + 2∑₍ᵢ<ⱼ₎ rᵢ·rⱼ + 1 )
```

### Reflected in Code

```python
linear[variables[i]] += P       # adds penalty per variable
quadratic[(r_i, r_j)] = 2 * P   # enforces exclusivity
offset = -2 * P + P             # normalizes constant term
```

---

This BQM formulation supports execution on classical or quantum annealers. While small in scale, it demonstrates how quantum-ready architectures can be applied to real pharmaceutical contracting scenarios.
