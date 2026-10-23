# Finite-shot verification of coherent replay waveform learning

This directory contains a reproducible two-qubit local-refinement experiment for the proposed waveform learner. It checks the exact echo orientation and response identity, implements genuine finite-shot product-Pauli process-shadow statistics, and reconstructs a noncommuting driven waveform that cannot be identified by endpoint-only experiments.

**What the result supports:** the signs, time ordering, process-estimator normalization, and finite-shot reconstruction mechanism work in this explicit small example. **What it does not establish:** the large-system theorem, optimal constants, a practical crossover, or robustness to decoherence, imperfect controls, schedule drift, or SPAM bias.

## Reproduce

From the repository root, install the pinned dependencies and run:

```bash
python3 -m pip install -r verification/requirements.txt
python3 verification/verify_protocol.py --output verification/generated/protocol.json
```

The recorded environment uses Python 3.12.14, NumPy 2.3.5 and SciPy 1.17.0. The committed reference [expected/protocol.json](expected/protocol.json) records the versions, random seeds, schedules, stage-by-stage errors, resource counts, shot-budget controls and scope limitations. A new run writes to `verification/generated/protocol.json`; this is also the default destination, so the committed reference is not overwritten. The script creates the output directory if needed.

The default run uses seeds 20261023 through 20261034. Finite-shot outcomes are sampled as multinomial **counts** over a small exactly enumerated outcome space. This classical shortcut avoids generating hundreds of millions of individual statevectors and does not reduce the physical shot cost.

## The calibration problem

Let $`x=2t-1`$, with $`0\le t\le1`$, and define

```math
\widehat H_0(t)=x(0.25XI+0.20ZZ+0.15IZ)
 +x^3(0.18IX+0.12YY).
```

The unknown schedule is $`H=\widehat H_0+R_0`$, where

```math
R_0(t)=0.05\big[(0.60x+0.25x^3)XI
 +(-0.40x+0.35x^3)ZZ
 +(0.30x-0.20x^3)IX\big].
```

Both schedules are degree-three polynomials on the same known five-term local interaction pattern. Their coefficient functions differ uniformly by 0.0425. They are not commuting schedules: the operator norm of $`[H(0.10),H(0.35)]`$ is approximately 0.02512.

Both satisfy $`H(1-t)=-H(t)`$. Substituting $`s=1-t`$ into the second half of the time-ordered evolution reverses the order and sign of the first half, giving

```math
U_H(1,1/2)=U_H(1/2,0)^\dagger,
\qquad U_H(1)=I.
```

The same holds for the nominal schedule. Therefore **no experiment with access only to the completed pulse can distinguish these schedules**, even with perfect endpoint process tomography, ancillas, or repeated applications. This is an exact identifiability statement; the numerical endpoint difference, $`2.35\times10^{-15}`$, is only a solver check. This elementary example is not itself a novelty claim.

Intermediate prefixes do distinguish the schedules. The largest sampled operator difference is 0.01189 near $`t=1/2`$. At $`t=0.375`$, one accessible signed input/output Pauli transfer is approximately $`-0.01715`$. Prefix access therefore reveals information that the endpoint omits.

The learner is not told to impose time antisymmetry. It fits all four degree-three Chebyshev coefficients for each of the five Hamiltonian terms, including even components that are absent from the true schedule. Its input is the nominal model and a supplied initial coefficient-error bound of 0.05. The coarse initializer is outside this experiment.

## Algebra and orientation checks

For a current model define the right echo

```math
E_t=U_H(t)U_{\widehat H}(t)^\dagger.
```

The known inverse acts first. For one fixed prefix, the code independently integrates the residual generator

```math
G_{t,s}=U_{\widehat H}(t,s)R(s)U_{\widehat H}(t,s)^\dagger
```

and compares its time-ordered evolution with the right echo. It computes $`L_t=\int_0^tG_{t,s}ds`$ by Gauss–Legendre quadrature, separately from the residual-evolution integration. It separately checks a symmetric finite-parameter derivative and

```math
R(t)=L_t'+i[\widehat H(t),L_t].
```

At $`t=0.63`$, the recorded checks are:

| Check | Numerical error |
|---|---:|
| Right echo versus independently integrated exact residual evolution | $`3.47\times10^{-13}`$ |
| Wrong left echo versus that same residual evolution | $`1.09\times10^{-3}`$ |
| Differential reconstruction identity, relative operator norm | $`9.26\times10^{-10}`$ |
| Quadrature response versus symmetric parameter derivative | $`1.37\times10^{-12}`$ |
| Process-shadow expectation versus direct Pauli transfer trace | $`2.82\times10^{-13}`$ |

For a one-site $`Q`$ anticommuting with a response Pauli $`P`$, the implementation uses $`B=iPQ`$, including its Pauli sign. It checks

```math
2^{-n}\operatorname{Tr}[Q E_t^q B E_t^{-q}]
 =2q\,2^{-n}\operatorname{Tr}(P L_t)+\text{remainder}.
```

With $`q=1`$, reducing the residual scale from 0.08 to 0.005 reduces the maximum transfer remainder quadratically. The ratio of remainder to squared residual scale stays between 0.01152 and 0.01157. This is evidence for the local expansion in this instance, not a numerical proof of its uniform bound.

## Genuine finite-shot data

Every simulated shot chooses independent random single-qubit input Pauli axes and eigenvalue signs, prepares the corresponding product state, applies $`E_t^q`$, and measures independent random single-qubit output Pauli axes. Intermediate controls may entangle the state; the unknown prefix need not receive a product input.

For input Pauli $`B`$ and one-site output $`Q`$, the process-shadow estimator multiplies the signed input-axis match weight $`3^{|B|}`$ by the signed output-axis match weight 3. Its expectation is the required transfer coefficient. The code verifies both that expectation and the second-moment upper bound $`3^{|B|+1}`$.

There are 36 possible product eigenstates for two qubits. The joint experiment has 1296 possible combinations of input state and output basis/outcome. Their exact Born probabilities are computed from the small dense matrices. The finite data are sampled using `rng.multinomial(N, probabilities)`; Gaussian perturbations of ideal coefficients are not substituted for measurement outcomes. All 15 nonidentity response coefficients share each batch of process-shadow data.

The learner uses Chebyshev–Lobatto nodes $`0,1/4,3/4,1`$, finite-difference spacing $`h=1/8`$, centered interior stencils, and three-point one-sided endpoint stencils. Its seven nonzero queried prefixes are

```math
\{1/8,1/4,3/8,5/8,3/4,7/8,1\}.
```

Each refinement estimates $`L_t`$, differentiates the estimate, adds the known commutator correction, and interpolates the residual coefficient functions. The mesh, amplification constant $`q\delta=0.10`$, and shot count are fixed across refinements. These instance-level numerical choices are not asserted to satisfy the conservative universal constants in the theorem.

Uniform errors are evaluated at the endpoints and all real derivative roots of each cubic coefficient error. This removes a finite-grid approximation; the roots are computed in floating point, not with interval certification.

## Finite-shot results and the actual cost

With 20,000,000 shots per nonzero prefix per stage, six stages use $`q=2,4,8,16,32,64`$. The first fixed-seed trajectory has the following error in the complete coefficient waveform:

| Echo count $`q`$ | Uniform waveform error | Next maintained target |
|---:|---:|---:|
| 2 | 0.006388 | 0.025000 |
| 4 | 0.002762 | 0.012500 |
| 8 | 0.002346 | 0.006250 |
| 16 | 0.000743 | 0.003125 |
| 32 | 0.000885 | 0.001563 |
| 64 | 0.000522 | 0.000781 |

Actual error need not decrease at every stochastic update; the maintained target halves at each stage. Across the 12 predetermined seeds, every observed stage remains within its next target. The final uniform errors range from 0.000193 to 0.000725, with median 0.000317. This observed 12/12 frequency is not a statistical guarantee.

Running the same stencils with exact transfer expectations gives final error $`8.71\times10^{-7}`$, showing that shot noise dominates the displayed finite-shot run. A separate fixed-seed budget control produces final errors 0.00659, 0.00128 and 0.000186 at respectively 100,000, 1,000,000 and 20,000,000 shots per prefix per stage. The two smaller budgets fail the final target.

**One default six-stage learning run costs:**

- 840,000,000 fresh product-state preparations and measurement shots;
- 17,640,000,000 unknown-prefix invocations;
- 10,080,000,000 units of total unknown evolution time, with the pulse horizon normalized to one;
- the same number of known-inverse invocations, with the same aggregate *target simulation time*;
- up to 64 coherent echoes per shot, corresponding to 128 units of requested unknown-plus-inverse evolution for the longest prefix if both can be executed at the normalized Hamiltonian rate.

The code does not compile those inverse controls into hardware gates. Requested simulation time is not a measurement of actual digital-controller execution time. The nominal initialization, compilation gates, hardware wall time and noise protection are omitted resources and are labeled as such in the JSON. These deliberately explicit costs preclude interpreting this run as a practical advantage demonstration.

## Limited precision-gain diagnostic

An additional calculation takes a single residual-amplitude parameter, keeps the prefix and product measurement scheme fixed, and compares $`q`$-fold echoes against independent unamplified $`q=1`$ echoes. The classical Fisher information in the complete product-shadow outcome distribution grows almost as $`q^2`$. At $`q=64`$, $`F_q/(q^2F_1)=0.999934`$, so information per unit of unknown evolution is approximately 63.996 times the $`q=1`$ value.

This confirms the coherent amplification mechanism for that one-dimensional local experiment. It does not optimize the independent-prefix learning baseline, account for controller synthesis, establish a multiparameter optimum, or demonstrate a practical crossover. It should not be cited as a general classical-versus-quantum speedup.

## Systematic controller-error diagnostic

A separate exact-expectation calculation replaces every ideal pair by

```math
E_{t,b}=E_t\exp(-ibZI).
```

The error rotation acts immediately before the nominal inverse in each pair. At one fixed prefix, the experiment compares a fixed angle $`b=2\times10^{-4}`$ with an angle $`b=0.004\delta`$, while $`q\delta=0.10`$ and the residual bound shrinks by factors of two. It reports the additional bias in every inferred response coefficient after division by $`2q`$.

This deliberately limited control check shows why controller accuracy must be paid: a fixed per-pair error gives an approximately fixed response-coefficient bias, so its size relative to the desired residual grows as the residual shrinks. Scaling the angle with the residual bound keeps that relative bias small in this example. The exact rows are in `systematic_controller_bias_diagnostic` in the JSON. This is neither a stochastic noise model nor a simulation of the complete waveform learner under noisy controls, and does not establish noise robustness.

| Residual scale | Echo count | Fixed-angle response bias / residual | Scaled-angle response bias / residual |
|---:|---:|---:|---:|
| 0.05 | 2 | 0.0039995 | 0.0039995 |
| 0.00009765625 | 1024 | 1.9907 | 0.0039990 |

The fixed-angle absolute response bias stays near $`2\times10^{-4}`$; the scaled-angle bias falls to $`3.91\times10^{-7}`$. These are response-coefficient biases at one prefix, not claimed errors of the full noisy waveform estimator.

## Files and integration scope

- `verify_protocol.py`: complete deterministic and finite-shot experiment.
- `expected/protocol.json`: committed reproducible reference results and resource records.
- `generated/protocol.json`: default output location for a new run.
- `requirements.txt`: exact NumPy/SciPy versions used to produce the saved reference results.

The experiment uses local code and fixed-seed random sampling.
