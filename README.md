# Quantum Rebate Optimization: PBM Tradeoff Modeling

This notebook implements a quantum-inspired optimization model to evaluate pharmaceutical rebate strategies under real-world market pressures. The example uses a Binary Quadratic Model (BQM) to assess the tradeoff between rebate generosity and the risk of triggering follow-on demands from competing Pharmacy Benefit Managers (PBMs).

## 🔍 Problem Statement

A large PBM is demanding a 10-point rebate increase to retain formulary status for a specialty drug. Other PBMs (representing 27% of market share) are likely to demand similar concessions if the offer is too generous. The goal is to identify the rebate percentage that minimizes **total financial impact**, considering both:

- Direct revenue loss from the rebate  
- Indirect exposure to spillover effects from other PBMs

## 🧠 Objective Function

We minimize a cost function expressed as:

minimize: L(r) + F(r) + P * (∑ xᵢ - 1)²


Where:
- `r` is the rebate level offered (from 1% to 10%)
- `L(r)` is the base projected revenue loss for offering rebate `r`
- `F(r)` is the estimated spillover cost if the rebate is too high (e.g. ≥ 9%)
- `xᵢ ∈ {0,1}` is a binary variable indicating if rebate level `i` is selected
- `P` is a penalty term enforcing one-hot selection of a single rebate level

This is implemented using the `dimod` library and solved exactly for small problem sizes.

## 📊 Output

The script prints:
- The optimal rebate % and its estimated total financial impact (in $M)
- A ranked table of the top 5 rebate strategies
- A bar chart visualizing total impact by rebate level

## 🧩 Notes

This model can be extended to:
- Include more PBMs or drugs
- Integrate real claims/utilization data
- Run on D-Wave quantum annealers via `dwave-system`

---

> Developed by Molly Maskrey · `github.com/mollymaskrey/Quantum`
