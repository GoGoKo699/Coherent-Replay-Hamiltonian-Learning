# Coherent Replay Hamiltonian Learning

**Can every local interaction be reconstructed throughout a driven pulse with total evolution time proportional to inverse precision?** For a known finite-range Pauli interaction pattern and polynomial coefficient waveforms on a fixed interval, coherent prefix replay gives such a learning algorithm.

The register stays coherent while a forward prefix of the unknown pulse is alternated with a compiled inverse of the current classical model. Product input and output probes reveal local response coefficients. A differential identity converts those responses into the instantaneous Hamiltonian, and successive refinements reduce the uniform waveform error.

For fixed local strength, geometry and degree $`m`$, the total unknown-evolution cost is

```math
\widetilde O\!\left(
\frac{\mathrm{poly}(m)\log(n/\rho)}{\epsilon}
\right),
```

including a paid coarse initializer. Here $`n`$ is the number of system qubits, $`\rho`$ the failure probability, and $`\epsilon`$ the maximum error of any coefficient function at any time. A single unknown static Pauli coefficient already requires $`\Omega(1/\epsilon)`$ unknown evolution time, so the precision exponent is optimal in this coherent access model.

| Resource or guarantee | Result and qualification |
|---|---|
| Output | Classical degree-$`m`$ polynomials for all known local Pauli terms, with uniform function error at most $`\epsilon`$ |
| Unknown evolution | Inverse-precision cost up to logarithms; a loose refinement degree factor is $`m^7`$ |
| Fresh preparations | Logarithmic growth in inverse precision, with polynomial degree and confidence factors |
| Coherent duration | A longest experiment uses order $`1/\epsilon`$ replayed echoes |
| Known inverse controls | Charged local lattice compilation: total $`\widetilde O(n\,\mathrm{poly}(m)/\epsilon)`$ gates, with ancillary workspace |
| Readout and classical data | At least linear in system size; the logarithmic shot count does not remove these costs |
| Access | Repeatable forward prefixes, coherent clock restart and switchable trusted controls |

## Read the science

Start with [the model and exact theorem](science/model.md). The proof then follows [the local response and echo bound](science/local_response.md), [waveform reconstruction](science/reconstruction.md), and [the full resource account](science/resources.md).

| To inspect | Read |
|---|---|
| Precise output, assumptions and access | [Learning task and theorem](science/model.md) |
| An extensive residual without a global-smallness assumption | [Uniform local echo expansion](science/local_response.md) |
| Product process probes, stable differentiation and contraction | [Reconstruction](science/reconstruction.md) |
| Initialization, compilation, precision, timing and lower bound | [Resources](science/resources.md) |
| Why endpoint calibration misses transient interactions | [Interpretation and worked example](science/interpretation.md) |
| Established mechanisms and closest competing algorithms | [Related work](references/RELATED_WORK.md) and [bibliography](references/references.bib) |
| Runnable calculations, actual costs and limits | [Verification](verification/README.md) |
| Question-to-file routes | [LLM reading guide](llms.txt) |

The useful inverse is

```math
H(t)-\widehat H(t)=L_t'+i[\widehat H(t),L_t],
\qquad
L_t=\int_0^t
U_{\widehat H}(t,s)\bigl(H(s)-\widehat H(s)\bigr)
U_{\widehat H}(t,s)^\dagger\,ds.
```

Locality controls the measured response even when the total residual Hamiltonian is extensive. Stable interpolation then recovers the coefficient functions throughout the interval.

## Reproduce the finite checks

From the repository root:

```bash
python3 -m pip install -r verification/requirements.txt
python3 verification/verify_protocol.py --output verification/generated/protocol.json
```

The two-qubit experiment independently checks the echo orientation, response identity, signed process estimator and finite-shot reconstruction. Its noncommuting true and nominal pulses have **exactly the same completed unitary**, while their intermediate prefixes differ.

All twelve predetermined simulation seeds and the smaller-shot failures are recorded. One default learning run represents **840 million fresh shots**; the program samples equivalent multinomial counts over the small outcome space. These explicit costs make it a verification of the mechanism, not a practical crossover demonstration. The written proofs and cited initialization/simulation theorems establish the asymptotic result.

## Scope and attribution

Learned-inverse amplification, adaptive control, process shadows, local Hamiltonian simulation and coherent sensing of reproducible commuting waveforms are established. The contribution developed here is a locally scalable differential inversion and error analysis for simultaneous noncommuting full-waveform learning. The [comparison](references/RELATED_WORK.md) makes the differing access and error metrics explicit.

The unknown drive must be repeatable while the same register remains coherent. Known controls and timing require precision that improves with the target error. Fixed per-replay noise or drift eventually limits amplification. The method does not assume an unknown inverse, a controlled unknown query, QRAM or a ground-state input. Intermediate query states can be entangled, and compiled controls use additional workspace.

The result concerns a closed system, a known interaction pattern, polynomial schedules and a fixed observation horizon. It does not claim a universal classical computational speedup, global diamond-distance tomography at local-learning cost, or a hardware advantage at the demonstrated sample counts.

## Purpose and contact

This repository serves as a record of the work and a guide for the author’s self-directed learning. For discussion or potential collaboration, please contact Ruge Lin at [gogoko699@gmail.com](mailto:gogoko699@gmail.com).
