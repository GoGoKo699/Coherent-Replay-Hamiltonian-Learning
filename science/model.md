# The learning task and exact claim

A calibrated final gate does not determine the interactions that occurred during its pulse. Different time-dependent Hamiltonians can have the same final propagator, even when their terms do not commute. Prefix experiments can resolve this ambiguity. The question is whether every local interaction waveform can be learned to precision $`\epsilon`$ using a total evolution time proportional to $`1/\epsilon`$, with resources that remain scalable in the number of qubits.

This account gives a constructive answer for polynomial waveforms on a finite-range lattice, provided that the unknown pulse can be replayed coherently and interleaved with compiled inverses of a learned model. The output consists of classical coefficient functions. The access condition and the cost of the known controls are part of the result.

## Reading route

| Question | Authoritative account |
|---|---|
| What is learned, and what access is required? | This page |
| Why can an extensive residual be amplified locally? | [Local response and echo bound](local_response.md) |
| How are transfer data converted into all coefficient waveforms? | [Reconstruction and contraction](reconstruction.md) |
| What do initialization, control, time, samples and output cost? | [Resources and precision lower bound](resources.md) |
| What does this allow in pulse calibration? | [Interpretation and examples](interpretation.md) |
| Which mechanisms and comparison algorithms are established? | [Related work](../references/RELATED_WORK.md) |
| What has been checked numerically? | [Verification](../verification/README.md) |

## 1. Hamiltonian family

Let $`n`$ qubits occupy a fixed-dimensional lattice with uniformly bounded site density. The known interaction pattern $`\mathcal A`$ consists of distinct nonidentity Hermitian Pauli strings $`P_a`$. Every string has weight at most $`k`$ and bounded geometric diameter. At most $`d`$ strings meet any one site. The dimension, density, interaction range, $`k`$, and $`d`$ are fixed independently of $`n`$, the polynomial degree, and the target precision. Consequently $`N=|\mathcal A|=O(n)`$.

In physical time, the unknown closed-system Hamiltonian is

```math
H_{\rm phys}(t)=\sum_{a\in\mathcal A}h^{\rm phys}_a(t)P_a,
\qquad 0\leq t\leq T.
```

Each real coefficient is a polynomial of degree at most $`m`$. The interval length $`T>0`$ and a bound on the local interaction strength are known. The identity Pauli is excluded: an additive time-dependent scalar changes only a global phase and cannot be identified by these experiments.

For the proofs, use the dimensionless coordinate $`x=t/T`$ and Hamiltonian $`H(x)=T H_{\rm phys}(Tx)`$. Rename $`x`$ as $`t`$, so that the proof interval is $`[0,1]`$ and

```math
H(t)=\sum_{a\in\mathcal A}h_a(t)P_a,
\qquad
\sup_{t\in[0,1]}\sup_i\sum_{a:\,i\in\mathrm{supp}(P_a)}|h_a(t)|\leq J.
```

The fixed dimensionless strength is the physical strength multiplied by $`T`$. In particular, every coefficient has supremum at most $`J`$. Constants below may depend on $`J`$ and the fixed geometry, and can grow rapidly with the physical horizon. The theorem is not uniform in a growing dimensionless strength $`J`$.

Write $`U_H(t,s)`$ for the time-ordered propagator from $`s`$ to $`t`$, and $`U_H(t)=U_H(t,0)`$. Schrödinger evolution uses $`\partial_t U_H(t)=-iH(t)U_H(t)`$.

## 2. Output and error

The output is a list of $`N`$ real polynomials $`\widehat h_a`$ of degree at most $`m`$, represented in a shifted Chebyshev basis. The success criterion is

```math
\Pr\!\left[
\max_{a\in\mathcal A}\sup_{0\leq t\leq1}
|h_a(t)-\widehat h_a(t)|\leq\epsilon
\right]\geq1-\rho,
\qquad 0<\rho\leq\frac13.
```

This is uniform error in the functions themselves. It does not use the poorly conditioned monomial-coordinate norm. A successful output contains $`O(N(m+1))`$ real numbers, with enough bits to preserve the stated function error. The classical output cost is therefore at least linear in $`n`$ whenever $`N=\Theta(n)`$.

For a requested physical coefficient error $`\epsilon_{\rm phys}`$, run the dimensionless theorem at $`\epsilon=T\epsilon_{\rm phys}`$ and divide the returned functions by $`T`$. Every normalized unknown-evolution time is multiplied by $`T`$. Thus the leading precision dependence remains $`1/\epsilon_{\rm phys}`$ at fixed $`T`$ and physical strength.

Local coefficient accuracy does not imply global diamond-distance accuracy of the same size. A direct global bound can lose a factor $`N`$. The theorem does not claim global process tomography at local-learning cost.

## 3. Operational access

An experimental shot starts with a product of single-qubit Pauli eigenstates. During the shot, the register remains coherent while the following operations are performed:

1. A known circuit approximately implements $`U_{\widehat H}(t)^\dagger`$, where $`\widehat H`$ is the current classical model.
2. The unknown drive executes the forward prefix $`U_H(t)`$ from the beginning of its classical schedule.
3. The pair is repeated $`q`$ times on the same quantum register.
4. Every system qubit is measured in a chosen single-qubit Pauli basis.

The classical drive clock can restart without resetting the quantum state. The unknown drive can be switched off or otherwise isolated while the trusted controls act. Its prefix dynamics are repeatable. The required prefix times depend on $`m`$ and the fixed physical parameters; refinement does not send the grid spacing to zero as $`\epsilon`$ decreases. The precision with which these times are realized does depend on $`\epsilon`$.

The ideal access model provides exact unknown prefixes. [The resource account](resources.md#implementation-accuracy-and-noise) gives sufficient error budgets for approximate controls, replay, timing and state preparation or readout. These are implementation requirements, not a theorem that fixed physical noise is harmless.

The inverse acts first, so a pair realizes the **right echo**

```math
E_t=U_H(t)U_{\widehat H}(t)^\dagger.
```

Only the inverse of the known model is required. There is no unknown inverse, no controlled unknown-unitary oracle, no QRAM, and no supplied ground state. The known inverse and previous repetitions can entangle the system before an unknown prefix. Product preparation describes the beginning of the whole shot, not every intermediate query input.

The controller's gates, numerical precision, classical data and ancillary qubits are counted. Product input and output probes themselves need no ancillary qubits. The full compiled implementation does use ancillary workspace.

## 4. Theorem: coherent-replay waveform learning

Fix the geometry and $`J`$ above. Assume the access of Section 3 and a trusted, efficiently computable local gate implementation of known polynomial Hamiltonian inverses. There is a randomized algorithm that returns the stated output with probability at least $`1-\rho`$.

Its paid coarse initialization uses the full-waveform learner of França, Rouzé, Werner and Möbus, specialized to an exact polynomial closed-system Hamiltonian. The required starting error $`\delta_0`$ is inverse-polynomial in $`m`$, independent of $`n`$ and the final precision. The [initialization argument](resources.md#paid-initialization) explains why both its sample and classical-processing costs are polynomial. This established initializer is a load-bearing ingredient, not an uncharged promise.

For $`0<\epsilon<\delta_0`$, let

```math
M=1+m^2,\qquad
\Lambda=2+\log(m+1),\qquad
K=\left\lceil\log_2\frac{\delta_0}{\epsilon}\right\rceil.
```

After initialization, the algorithm uses at most

```math
Q=O\!\left(
\frac{(m+1)M^3\Lambda^6}{\epsilon}
\log\frac{C_0 n(m+1)\max\{K,1\}}{\rho}
\right)
```

unknown prefix calls. Here and below constants include the fixed local Pauli-probe factor $`3^{2k}`$. Total normalized unknown-evolution time is at most $`Q`$. The number of fresh product-state preparations is at most

```math
S=O\!\left(
(m+1)M^4\Lambda^8 K
\log\frac{C_0 n(m+1)\max\{K,1\}}{\rho}
\right).
```

A longest shot contains $`O(\tau/\epsilon)`$ coherent echo repetitions, where the fixed amplification scale $`\tau`$ is specified in [reconstruction](reconstruction.md). The constants in these deliberately conservative bounds are not a prediction of practical sample counts. The degree dependence is not claimed optimal.

For fixed-dimensional finite-range lattices, established high-precision Hamiltonian simulation compiles the known controls using a total of

```math
\widetilde O\!\left(\frac{n\,\mathrm{poly}(m)}{\epsilon}
\log\frac1\rho\right)
```

local gates, in addition to the paid initialization. Polynomial factors for schedule evaluation and timing arithmetic are included. The implementation uses the $`n`$ system qubits and additional compiler workspace; a conservative bound is $`O(n\,\mathrm{poly}(m,\log(n/\epsilon)))`$ qubits. The lattice simulation theorem itself uses a constant number of ancillas per site. No ancilla-free gate claim is made.

Fresh-shot preparation, measurement and classical processing have at least their linear-in-$`n`$ cost. The logarithmic dependence on $`n`$ in $`Q`$ and $`S`$ concerns the number of parallel experimental shots, not the complete physical or classical workload. Precision-dependent controller synthesis and output bits are detailed in [resources](resources.md).

For fixed geometry, horizon and degree, the precision exponent in total unknown-evolution time is optimal: even a single unknown static Pauli coefficient requires $`\Omega(1/\epsilon)`$ time at constant success probability. The proof allows arbitrary known controls and adaptive decisions. It does not prove optimal logarithms, degree dependence, gate count or noise tolerance.

### Proof structure

The [local response identity](local_response.md) expresses the right echo as evolution under a dressed residual. Lieb–Robinson locality gives an interaction decomposition whose first support-size moment is uniformly $`O(\delta)`$ when every residual coefficient is at most $`\delta`$. An exact second-order Heisenberg expansion then bounds the error of any required local probe by $`O((q\delta)^2)`$, independently of $`n`$.

Random product process probes estimate the relevant transfer coefficients in parallel. Their linear terms reveal local coefficients of an integrated response $`L_t`$. The identity

```math
H(t)-\widehat H(t)=L_t'+i[\widehat H(t),L_t]
```

gives a constructive waveform inverse. Markov's polynomial inequality controls the finite-difference bias; stable Chebyshev interpolation converts nodal errors to a uniform function bound. One stage halves the coefficient error with a shot count independent of $`\delta`$. Its coherent repetitions grow as $`1/\delta`$. Summing the geometric refinement stages yields the stated precision law. [The contraction proof](reconstruction.md) includes confidence allocation, endpoints, degree zero, rounding and bounded controls on unsuccessful histories.

## 5. Contribution and boundary

Learned-inverse amplification, adaptive quantum control, classical process probes, local simulation and coherent sensing of reproducible commuting waveforms are established ingredients. The contribution developed here is their combination with an explicit local differential inverse and an extensive-system error bound for simultaneous, noncommuting full-waveform learning. [Related work](../references/RELATED_WORK.md) separates these ingredients from the resulting task and access model.

The independent-prefix baseline has weaker experimental access. Improving its precision exponent by coherent replay is an operational resource trade, not a same-access speedup over a lower bound that forbids those controls. The result does not establish an exponential advantage over all classical computation, a practical crossover on current hardware, or a noisy open-system extension.
