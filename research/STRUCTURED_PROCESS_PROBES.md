# Structured process probes: a sampling-cost refinement

The baseline [local response protocol](../science/local_response.md#5-product-state-transfer-estimator) uses independent uniformly random input and output Pauli axes. For a target signed Pauli input (B=\sigma_B\bigotimes_{j\in S}B_j) and a one-site output (Q), its unbiased process-shadow estimator has second moment (3^{|S|+1}). This is a worst-case constant at fixed locality, but it can be expensive in a finite calibration run.

## A deterministic-setting estimator

For **one target pair** ((B,Q)), fix the input measurement/preparation axes on (S) to those of (B), and fix the output measurement axis on the site of (Q). Prepare independent uniformly random eigenvalue signs (s_j\in\{-1,1\}) for (j\in S). On every other input qubit prepare an independent randomized single-qubit state with mean (I/2). Let (y\in\{-1,1\}) be the measured eigenvalue of (Q). Define

```math
Z_{B,Q}^{\mathrm{target}}=\sigma_B\left(\prod_{j\in S}s_j\right)y.
```

The random input ensemble obeys

```math
\mathbb E\!\left[\sigma_B\left(\prod_{j\in S}s_j\right)\rho_{\mathrm{in}}\right]
=\frac{B}{2^n}.
```

Consequently, for **any** quantum channel \(\mathcal E\), including a repeated echo,

```math
\mathbb E Z_{B,Q}^{\mathrm{target}}
=2^{-n}\mathrm{Tr}\!\left[Q\mathcal E(B)\right]
=f_{B,Q},
\qquad
\mathbb E\left[(Z_{B,Q}^{\mathrm{target}})^2\right]=1.
```

This is a strict reduction of the *single-target second moment* from (3^{w+1}) to 1, without a new quantum access assumption. The variance is (1-f_{B,Q}^2), and Hoeffding's inequality gives at most (2\eta^{-2}\log(2/\beta)) shots to attain additive accuracy \(\eta\) with failure probability \(\beta\) (a deliberately conservative constant).

## Compatibility and the simultaneous-output cost

Two target pairs are compatible in one shared fixed-setting experiment if (i) their nonidentity input Pauli factors agree wherever their supports overlap and (ii) their output Pauli axes agree if they address the same output site. On each qubit appearing in any input target, prepare a random eigenstate of that common axis; on other qubits randomize a state with mean (I/2). Choose all output axes consistently. Each compatible target has its own product-of-input-signs estimator, still bounded by one.

Build a **conflict graph** with one vertex per target pair and an edge for every incompatible pair. A proper coloring with \(g\) colors partitions the targets into \(g\) simultaneously measurable groups. If every group receives \(N\) independent shots, a union bound gives

```math
N\ge\frac{2}{\eta^2}\log\frac{2M_{\mathrm{tar}}}{\beta},
\qquad
S_{\mathrm{structured}}\le
\frac{2g}{\eta^2}\log\frac{2M_{\mathrm{tar}}}{\beta}
\quad\text{(up to integer ceilings)}.
```

The original uniform random-axis estimator uses \(O(3^{w_{\max}+1}\eta^{-2}\log(M_{\mathrm{tar}}/\beta))\) **shared** shots. Therefore the single-target factor (3^{w+1}) is *not* automatically a full-algorithm speedup: it must be compared against the number of compatible groups \(g\). For a bounded-incidence, bounded-weight local target family, each target conflicts with at most a constant number of others (depending on the fixed geometry), so greedy coloring gives a constant \(g\) independent of \(n\). This preserves logarithmic shot dependence on system size, but whether it improves the fixed constant depends on the actual target pattern and confidence constants.

A safe implementation should explicitly construct the target pairs (B=iPQ,Q), include the sign of (B), color the conflict graph, and compare *measured* confidence intervals and total physical shot counts against the original randomized-shadow protocol. The signed target estimator remains valid for entangling echo channels; the input is product only at the beginning of a shot.

## Boundaries and next decisive test

1. This is a **proved estimator and grouping construction**, not yet a verified reduction of the project's 840-million-shot run. The earlier experiment's stencils, inverse-control costs, and coarse initializer remain unchanged.
2. The original theorem's asymptotic \(\widetilde O(1/\epsilon)\) unknown-evolution precision law is unchanged. A fixed-geometry coloring can improve constants, not its exponent.
3. A graph coloring minimizes the number of uniform-allocation groups only approximately; heterogeneous target variances, covariance-aware joint reconstruction and optimized allocation across time settings may improve the full budget further.
4. The next discriminating experiment is to enumerate the actual target pairs at every prefix in the existing two-qubit verification, compute the minimum compatible grouping, and run paired finite-shot trials with **equal total shots** and identical seeds. Compare final uniform waveform error and success frequencies, including controller cost. Do not claim a hardware crossover from this analytic bound.

This note supplements the existing proof and numerical record. It does not replace the certified baseline or change the educational milestones.
