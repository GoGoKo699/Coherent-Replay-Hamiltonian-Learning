# Resources, implementation accuracy and precision optimality

The useful resource trade is between repeated independent prefix experiments and a longer coherent experiment on one register. Amplification reduces the number of fresh preparations needed at finer precision, while increasing coherent duration and the accuracy required of every replayed control. This page counts both sides of that trade.

All formulas use the normalized interval and coefficient error defined in [the model](model.md). Fixed constants may depend on the dimensionless strength $`J`$, geometric range, coordination and local Pauli weight.

## Refinement resources

[Reconstruction](reconstruction.md) fixes a known constant $`C\geq1`$ and

```math
M=1+m^2,\qquad \Lambda=2+\log(m+1),
\qquad h=\frac{1}{128CM\Lambda},
```

```math
\tau=\frac{h}{128C\Lambda},\qquad
\eta=\frac{\tau h}{128\Lambda},\qquad
\delta_0=\frac{\tau}{2}.
```

Here $`h`$ is the finite-difference spacing, $`\tau`$ limits the amplified residual, and $`\eta`$ is the required absolute transfer-coefficient accuracy. None depends on the final $`\epsilon`$ or on $`n`$. The constants are chosen to make a complete contraction proof simple; they are not optimized experimental settings.

At stage $`j`$, the maintained error is $`\delta_j=2^{-j}\delta_0`$ and

```math
q_j=\left\lfloor\frac{\tau}{\delta_j}\right\rfloor,
\qquad \frac{\tau}{2}\leq q_j\delta_j\leq\tau.
```

At most $`2(m+1)`$ prefix times supply the interpolation nodes and their one-sided stencils. A time-zero response is known exactly and need not be measured. At each nonzero time, one ensemble of product-input/product-output shots estimates all $`O(n)`$ required transfer entries. Each entry has variance at most $`3^{2k}`$. Bernstein's inequality and a union bound permit

```math
B=O\!\left(
3^{2k}\eta^{-2}
\log\frac{C_0 n(m+1)\max\{K,1\}}{\rho}
\right)
```

shots per time and stage, where $`K=\lceil\log_2(\delta_0/\epsilon)\rceil`$. The initialization and refinement receive separate failure budgets. A union bound does not require the estimates of different Pauli coefficients from the same shot to be independent.

The last maintained error satisfies $`\delta_K\leq\epsilon`$ and $`\delta_{K-1}>\epsilon`$. Therefore

```math
\sum_{j=0}^{K-1}q_j
\leq\tau\sum_{j=0}^{K-1}\frac1{\delta_j}
<\frac{2\tau}{\epsilon}.
```

Multiplying by the number of prefix times and shots gives

```math
Q=O\!\left(
(m+1)3^{2k}\frac{\tau}{\eta^2\epsilon}
\log\frac{C_0 n(m+1)\max\{K,1\}}{\rho}
\right).
```

Since $`\tau/\eta^2=O(\Lambda^3 h^{-3})`$, this is the bound in [the theorem](model.md#4-theorem-coherent-replay-waveform-learning): a loose $`\widetilde O(m^7/\epsilon)`$ refinement count at large degree. Each prefix lasts at most one normalized time unit, so the same expression upper-bounds total unknown-evolution time. Physical time is restored by multiplying prefix durations by $`T`$.

The number of fresh preparations is $`S\leq2(m+1)BK`$. It grows logarithmically with inverse precision apart from the confidence logarithm. The longest coherent shot instead contains $`O(\tau/\epsilon)`$ pairs. These are different resources and cannot be interchanged in a hardware comparison.

## Paid initialization

The algorithm needs an initial degree-$`m`$ model with coefficient-function error at most $`\delta_0`$. This is supplied by the independent-prefix full-waveform learner [F2026](../references/RELATED_WORK.md#f2026), with failure probability at most $`\rho/2`$. Its closed-system specialization matches the present known-pattern, bounded-locality model. Use the raw degree-$`m`$ polynomial interpolants, with numerical error included in the initialization budget; pointwise clipping would leave the required polynomial class.

The dependence on degree requires care. In Corollary 5.1 of F2026, exact polynomial schedules have zero approximation modulus. At internal accuracy $`\zeta`$, the analytic localization radius is $`r=O(1+\log(1/\zeta))`$, and the localized generator norm grows as $`O(r^D)`$. Its auxiliary polynomial degree is

```math
d_{\rm aux}=(m+1)L,\qquad
L=O\!\left(r^D+\log\frac{1+r^D}{\zeta}+1\right).
```

At the inverse-polynomial starting error $`\delta_0`$, internal accuracy can be chosen inverse-polynomial in $`m+1`$, with logarithmic corrections. Thus $`L`$ is polynomial in $`\log(m+2)`$ for fixed $`D`$, and $`d_{\rm aux}=\operatorname{poly}(m+1)`$. Polynomial derivative and interpolation factors can be absorbed by choosing a sufficiently small such $`\zeta`$.

Crucially, this growing localization region certifies an approximation; the algorithm does not enumerate its entire Hilbert space. The actual inverse-probe semidefinite programs in Sections 6 and 7 use fixed isolation tolerances and constant-size regions for fixed geometry and horizon. Their size does not grow with the final $`\epsilon`$. Consequently the paid initializer has $`\operatorname{poly}(m+1)\log(n/\rho)`$ sample cost and polynomial classical processing in $`n,m,\log(1/\rho)`$. Its potentially large fixed-horizon constants remain part of the cost.

If $`\epsilon\geq\delta_0`$, this initializer alone already meets the target. There is no inverse-precision refinement cost in that branch. The result relies on F2026's established initialization theorem; it does not claim a new initializer or experimentally demonstrate its large-system implementation.

## Compiling the known inverse

At any stage, the current polynomial model is an explicit classical list. A guard keeps every accepted coefficient bounded by a fixed constant, including on unsuccessful statistical histories. The inverse is the time-ordered evolution generated by the reversed negative schedule

```math
H_{\rm inv}(s)=-\widehat H(t-s),\qquad 0\leq s\leq t.
```

Only known coefficients enter this simulation. A circuit is compiled once for each model and prefix time and then reused for the $`q_j`$ repetitions. A classical loop can represent the repetitions, but every executed gate is still charged.

For a finite-range lattice, [HHKL2020](../references/RELATED_WORK.md#hhkl2020), Theorem 1, gives near-linear gate count in volume and simulation duration, with polylogarithmic accuracy dependence for efficiently computable, piecewise slowly varying local terms. A bounded degree-$`m`$ polynomial has derivative $`O((1+m^2)J)`$ by Markov's inequality. Polynomial time rescaling makes it satisfy the theorem's smoothness convention. Polynomial evaluation in a stable basis, finite-precision arithmetic and local circuit synthesis contribute polynomial factors in $`m`$ and logarithmic factors in the requested accuracy.

For one inverse with operator error at most $`\nu`$, this supplies a bound of the form

```math
C_{\rm inv}(n,m,\nu)
=\widetilde O\!\left(n\,\operatorname{poly}(m+1)\right),
```

where the suppressed logarithms include $`n/\nu`$. The total control count is $`\sum_{j,t} Bq_j C_{\rm inv}(n,m,\nu_j)`$. It has the precision exponent one up to logarithms. The simulator's extra qubits and their preparation are counted; its lattice layout uses a constant number of ancillary qubits per system site, with further workspace for the selected arithmetic implementation.

No global constant-cost coefficient oracle is presumed. The local blocks have only polylogarithmically many sites at the required global accuracy. Their known coefficient tables can be compiled by explicit arithmetic and selection circuits, charging their size. The complete model has $`O(n(m+1))`$ entries and must be stored and supplied to the controller. An implementation on a general nongeometric graph should retain the explicit function $`C_{\rm inv}`$; the lattice gate theorem does not establish the same cost for every sparse graph.

These are logical circuit resources under the trusted-control model. A particular hardware architecture must additionally supply coherent execution and whatever physical error suppression is needed. The availability of accurate known gates alone does not guarantee that an unknown driven Hamiltonian can be replayed without noise.

## Classical work, readout and storage

A product shot requires $`O(n)`$ system preparation and measurement operations. The signed weights for $`O(n)`$ fixed-support probes can be processed in $`O(n)`$ work per shot, up to fixed local factors. Accumulating means and confidence bounds needs no full $`2^n`$-dimensional state or process matrix. Correlated estimates share data but retain individual error guarantees.

Degree-$`m`$ interpolation, evaluation, guard checks and coefficient rounding take polynomial time in $`m`$ for each interaction. The initializer has its own polynomial classical cost. Controller synthesis is also charged, separately from the hardware gate executions. None of these statements reduces the complete runtime to $`O(\log n)`$.

A shifted Chebyshev polynomial satisfies $`|T_r(2t-1)|\leq1`$. Rounding each of its $`m+1`$ coefficients to error at most $`\delta/[16(m+1)]`$ changes its waveform by at most $`\delta/16`$. Allocate another $`\delta/16`$ uniform error to the finite-precision interpolation and commutator arithmetic, for a joint numerical budget $`\delta/8`$ as in the contraction proof. Stable interpolation and explicit fixed-support sums permit this accuracy with polynomial arithmetic cost. The final output therefore requires

```math
O\!\left(n(m+1)\log\frac{C(m+1)}{\epsilon}\right)
```

classical bits for bounded coefficients, with fixed-strength constants absorbed. Coefficient evaluation and gate compilation may need additional $`\log n`$ precision to control a global inverse error; this is not silently folded into the output's local error metric.

Wall-clock cost also includes the time for known gates and clock resets. If one reset costs $`t_{\rm reset}`$, add $`Qt_{\rm reset}`$. Gate depth, memory lifetime and calibration overhead determine whether the experimental resource reduction is useful on a specific device.

## Implementation accuracy and noise

The ideal theorem is for exact repeatable unknown prefixes. A useful robust formulation bounds the implemented channel for **each complete echo pair** in diamond norm:

```math
\|\widetilde{\mathcal E}_{j,t}-\mathcal E_{j,t}\|_\diamond\leq\mu_j,
\qquad
\mu_j\leq\frac{\delta_jh}{128\Lambda}.
```

Telescoping $`q_j`$ channel uses gives a defect at most $`q_j\mu_j`$ in a normalized transfer coefficient. Division by $`2q_j`$ removes the factor $`q_j`$, and finite differentiation costs $`O(1/h)`$. The resulting error fits the contraction budget. The per-pair condition applies uniformly on the actual history. It also suffices for individually different pairs with the same bound; uncontrolled memory across pairs is outside this channel model.

A known inverse implemented to operator error $`\nu_j`$ has channel error at most $`2\nu_j`$. Budgeting this and the unknown-prefix defect separately, for example with $`\nu_j\leq\mu_j/4`$ and unknown-prefix diamond defect at most $`\mu_j/2`$, is sufficient. Thus control precision must improve proportionally to the maintained coefficient error, with the degree factors shown. High-precision simulation changes the gate count only polylogarithmically; it does not make physical control errors disappear.

### Timing and schedule reproducibility

A fixed grid is not a fixed timing-accuracy guarantee. For an endpoint error $`\Delta t`$, a conservative global bound is

```math
\|U_H(t+\Delta t)-U_H(t)\|
\leq NJ|\Delta t|
```

when the schedule is defined over the perturbed interval. For a bounded internal clock perturbation, Markov's inequality gives a coefficient change of at most $`2m^2J|\Delta t|`$ on the normalized interval. Integrating the global generator difference and combining these effects gives a sufficient channel-error bound of order $`NJ(1+m^2)|\Delta t|`$.

Accordingly, the conservative sufficient timing resolution is

```math
|\Delta t|\leq
c\,\frac{\delta_jh}{\Lambda NJ(1+m^2)}.
```

This is a global sufficient condition, not a necessary local-noise threshold. The required digital clock description has logarithmic bit length in $`n/\epsilon`$, but actual jitter and drift must obey the physical bound. Similarly, a coefficient perturbation of size $`\xi`$ during each replay admits the sufficient global bound $`O(N\xi)`$ per unit prefix. The present theorem does not turn fixed replay drift into vanishing estimation error.

### Preparation, readout and a fixed noise floor

For a fixed probe, the process weight has absolute value at most $`3^{2k}`$. A bounded total-variation defect in a whole shot's preparation/readout distribution therefore gives a corresponding bounded additive bias in its transfer mean. Keeping this bias below a fixed fraction of $`\eta`$ suffices. This is a calibrated-bias condition, not a protocol for discovering or removing arbitrary unknown SPAM errors.

Per-pair decoherence is more restrictive because it occurs inside the amplified sequence. For example, in a commuting one-qubit experiment, a transverse signal acquires a visibility factor $`e^{-q\gamma t}`$ under dephasing rate $`\gamma`$. At fixed nonzero $`\gamma`$, letting $`q`$ grow as $`1/\epsilon`$ eventually removes the amplified signal. The coherent theorem gives no asymptotic Heisenberg scaling at fixed per-replay noise. The finite-shot verification includes a controlled per-pair error example to expose this budget rather than imply general noise tolerance.

## Precision lower bound

The Hamiltonian family contains the one-parameter subfamily

```math
H_\theta(t)=\theta P,
```

where $`P`$ is one fixed one-site Pauli and every other coefficient is zero. Choose two allowed values separated by $`4\epsilon`$. Their output error balls of radius $`\epsilon`$ are disjoint, so a successful learner with failure probability at most $`1/3`$ distinguishes the two cases with constant advantage.

For an unknown evolution of duration $`t`$,

```math
\|e^{-i\theta Pt}-e^{-i\theta'Pt}\|
\leq |\theta-\theta'|t.
```

A hybrid argument replaces one unknown use at a time in any controlled adaptive protocol. Known controls are the same parameter-independent maps at each branch; measurements may be deferred into a classical record. Contractivity and the triangle inequality bound the final channel distance by

```math
2|\theta-\theta'|\,\mathcal T_{\rm unknown},
```

where $`\mathcal T_{\rm unknown}`$ is the sum of unknown-evolution durations along the charged experiment. A worst-case bounded-time protocol therefore needs $`\mathcal T_{\rm unknown}=\Omega(1/\epsilon)`$ to distinguish the pair. The same lower bound holds for bounded expected resource with standard constant-factor truncation. Arbitrarily accurate known controls do not evade it.

For comparison, suppose each shot has a fresh state, one prefix of duration at most one, and a final measurement, with no quantum memory carried between shots. For the same two static parameters, the output states of one shot have fidelity at least $`1-O(\epsilon^2)`$: the two unitaries differ by a rotation through angle at most $`4\epsilon`$. Any measurement therefore produces conditional outcome distributions with squared Hellinger distance $`O(\epsilon^2)`$. This bound holds for every preparation and measurement chosen from the earlier classical record. The chain bound for sequential classical experiments then gives squared Hellinger distance at most $`O(S\epsilon^2)`$ for $`S`$ shots. Constant distinguishing advantage requires $`S=\Omega(\epsilon^{-2})`$. This two-point argument does not assume an unbiased estimator. Coherent replay changes the experiment model; the lower bound for the weaker model is not asserted against the stronger one.

The lower bound fixes the coefficient-amplitude task and the replayed horizon. Time-dependent frequency-estimation examples whose generator sensitivity grows with a longer physical horizon can have different time powers, as in [P2017](../references/RELATED_WORK.md#p2017). That is a different parameter and resource limit.

## What the resource result establishes

The precision exponent one survives charging polynomial initialization, all local readout, the classical model and high-precision inverse compilation. The proof does not optimize degree dependence or fixed constants. It gives an asymptotic coherent experimental-resource advantage for an extensive waveform output. The small-system calculations in [verification](../verification/README.md) check algebra, sampling and error accumulation; their large explicit shot counts do not establish a practical advantage over an optimized independent-prefix experiment.
