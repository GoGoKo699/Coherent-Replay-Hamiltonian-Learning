# Full pulse calibration and the meaning of the precision gain

The output of the algorithm is a time-resolved local generator. It answers which interaction was present, how strongly it acted, and when during the pulse it occurred. That information can matter even when the completed gate has already been characterized exactly.

[The theorem](model.md) concerns a known local interaction pattern, bounded polynomial waveforms on a fixed interval, and repeatable coherent access. It supplies an asymptotic precision law under those conditions. The examples below explain the scientific use and the distinction between that law and an experimentally useful implementation.

## Identical final gates can hide different noncommuting waveforms

Consider any Hamiltonian satisfying

```math
H(1-t)=-H(t),\qquad 0\leq t\leq1.
```

Changing variables in the second half of its time-ordered evolution reverses the order and sign of the first half. Hence

```math
U_H(1,1/2)=U_H(1/2,0)^\dagger,
\qquad U_H(1)=I.
```

No commutativity assumption is used. A simple polynomial family is

```math
H(t)=xA+x^3B,\qquad x=2t-1,
```

with arbitrary local Hermitian $`A,B`$. When $`[A,B]\ne0`$, Hamiltonians at different times generally do not commute. Nevertheless every member of this family has exactly the same final unitary.

Any experiment restricted to the completed channel therefore obtains identical data for these different schedules. Ancillas, perfect process tomography and repeated completed pulses cannot resolve the ambiguity. Prefix access does: generally $`U_H(t)`$ differs at intermediate $`t`$. Full-waveform learning can identify transient fields and couplings that cancel before the pulse ends.

This elementary identifiability example motivates the output. It is not the novelty of the coherent-replay theorem, which also handles general bounded noncommuting polynomial schedules without imposing time antisymmetry.

## A finite-shot two-qubit reconstruction

The [verification program](../verification/verify_protocol.py) uses the nominal model

```math
\widehat H_0(t)=x(0.25XI+0.20ZZ+0.15IZ)
+x^3(0.18IX+0.12YY),\qquad x=2t-1,
```

and true residual

```math
R_0(t)=0.05\left[
(0.60x+0.25x^3)XI
+(-0.40x+0.35x^3)ZZ
+(0.30x-0.20x^3)IX
\right].
```

The unknown schedule is $`H=\widehat H_0+R_0`$. The coefficient-function distance between the true and nominal models is $`0.0425`$. Both completed propagators are exactly the identity by the preceding argument. Their intermediate prefixes are different. The commutator norm $`\|[H(0.10),H(0.35)]\|\simeq0.02512`$ also confirms that this is a noncommuting example.

The learner is given a nominal model and a starting error bound $`0.05`$. It fits all four degree-three Chebyshev coefficients for each of the five known Pauli terms, including even components absent from the true waveform. It is not told to exploit the time antisymmetry.

The finite-shot experiment uses actual product-Pauli outcome distributions and multinomial sampling. One batch estimates all fifteen nonidentity two-qubit response coefficients. The small Hilbert space permits exact enumeration of the possible input/basis/outcome combinations; sampling their counts is computationally fast but represents the full physical number of shots.

The illustrative spacing $`h=1/8`$, amplification $`q\delta=0.10`$, and higher-order finite-difference stencils are selected for this instance. They differ from the conservative first-order universal proof settings. The supplied nominal model replaces the paid coarse initializer in this check. Thus the computation validates a local refinement mechanism, not a complete hardware execution of every theorem component.

With twenty million shots per nonzero prefix per stage, the first predetermined seed gives:

| Echo repetitions | Uniform waveform error after the update | Next declared error radius |
|---:|---:|---:|
| 2 | 0.006388 | 0.025000 |
| 4 | 0.002762 | 0.012500 |
| 8 | 0.002346 | 0.006250 |
| 16 | 0.000743 | 0.003125 |
| 32 | 0.000885 | 0.001563 |
| 64 | 0.000522 | 0.000781 |

Errors are maximized at the endpoints and real derivative roots of each cubic coefficient error, using floating-point arithmetic. They are not maxima over a sparse time grid. The stochastic error need not decrease at every update; the declared radius does halve. All twelve consecutive, predetermined seeds are retained in [the stored results](../verification/expected/protocol.json). Their final errors range from approximately $`1.93\times10^{-4}`$ to $`7.25\times10^{-4}`$, with median $`3.17\times10^{-4}`$. Twelve observed successes do not establish a universal confidence guarantee.

One six-stage run represents **840 million fresh preparations**, **17.64 billion unknown-prefix calls**, and **10.08 billion normalized units of unknown evolution time**. It also requests 17.64 billion known inverses. Their digital compilation and actual hardware execution are not simulated. Reducing the shot budget to one million or one hundred thousand per setting fails the same final target in the recorded budget-control experiment.

These costs are essential to interpreting the result. The example supports the algebra and finite-shot reconstruction; it does not demonstrate a practical resource advantage. The exact-expectation run has a much smaller final error, showing that shot noise dominates these chosen settings. [Verification](../verification/README.md) documents the full calculation, its deterministic checks and all resource omissions.

## Why replay changes the precision dependence

At one refinement stage, a current error bound $`\delta`$ is already known with high probability. A single residual echo changes a suitable local transfer coefficient by $`O(\delta)`$. Estimating that change with independent short shots requires a number of observations growing as $`1/\delta^2`$.

Coherently repeating the residual echo $`q=\Theta(1/\delta)`$ times produces a fixed-size signal. The [local remainder bound](local_response.md) keeps its nonlinear bias controlled when $`q\delta`$ is a sufficiently small fixed constant. The number of fresh observations for one refinement then stops depending on $`\delta`$, while each observation's coherent duration grows as $`1/\delta`$.

The crucial many-body step is local control of the bias. A residual with small coefficients can still have global norm proportional to $`n\delta`$. Treating the entire unitary as a single small perturbation would lose the desired size dependence. The weighted local interaction bound avoids this global smallness requirement. The subsequent differential identity recovers the instantaneous coefficients, rather than only an effective generator of one completed pulse.

This explanation should not be read as claiming that coherent multipass sensing or learned-inverse amplification originated here. [The related-work account](../references/RELATED_WORK.md) includes both established mechanisms and prior waveform-estimation experiments.

## A meaningful implementation comparison

The independent-prefix full-waveform learner and the coherent-replay learner have different access requirements. The former needs fresh product probes, one selected forward prefix and product readout. The latter preserves coherence across many prefixes and supplies accurate known inverse controls. The weaker-access learner also has a weak-dephasing extension absent from the present unitary theorem.

A hardware comparison must count the full cost per coherent pair. Schematically, if an independent-prefix implementation costs $`A/\epsilon^2`$ and a coherent implementation costs $`B/\epsilon`$ after initialization, then a formal crossover requires $`\epsilon<A/B`$. Gate execution, clock resets, data collection and compilation alter $`A`$ and $`B`$. A physical noise floor imposes a competing minimum attainable precision. An experimentally useful advantage requires an interval where both conditions hold. The asymptotic theorem alone does not show that this interval is nonempty for a particular device.

The finite example also computes a one-parameter Fisher-information diagnostic using a fixed prefix and fixed product measurement ensemble. Its near-quadratic growth with replay count checks coherent signal amplification. It is not an optimization over independent-prefix designs, a multiparameter optimality result or a complete cost comparison.

## Consequential boundaries

The interaction pattern and polynomial degree are supplied. Learning an unknown support, a nonpolynomial function class, or arbitrary open-system dynamics requires additional arguments. All coefficients are learned in the uniform function norm, while every final waveform is explicitly stored and processed. A logarithmic experimental shot count in system size does not remove the linear output and measurement costs.

The horizon and local strength are fixed. The locality constants may become large on longer intervals. Replaying the classical schedule on a coherent register is available only on devices that can perform that operation; it does not describe an irreversible drift trajectory that cannot be restarted.

Finally, the precision law concerns coherent quantum experimental resources. A digital classical algorithm cannot itself query an unknown quantum device without an experimental access model, and the present theorem does not establish a general exponential separation from classical computation. Its operational result is a scalable route from prefix data to a classical local waveform model with optimal inverse-precision unknown-evolution cost under the stated access.
