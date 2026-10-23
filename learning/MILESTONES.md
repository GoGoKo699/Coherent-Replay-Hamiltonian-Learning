# Thirty milestones for coherent replay waveform learning

This map follows the scientific question: how can repeated, controlled prefix experiments recover every local interaction throughout a driven pulse with inverse-precision evolution cost? It maps the current result, its proof and its physical meaning. The [learning entrypoint](README.md) and [source-to-project bridge](BRIDGE.md) provide complementary routes into the same account.

The allocation is **11 background/preliminaries milestones and 19 narrative/innovation milestones**. The background moves from a single observable to the complete experimental and statistical problem. The narrative needs more space because the result joins several distinct arguments: local control of an extensive residual, measurable response extraction, stable temporal inversion, adaptive contraction and a complete resource comparison. M11 and M30 synthesize their respective phases. Dependencies identify earlier milestones, rather than a separate reading curriculum.

The sole educational anchor is **Nielsen and Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition (2010)**. Section numbers are checked against the [publisher's contents][nc-contents]; its links below identify the relevant contents pages, not freely available chapter text. The textbook supplies quantum-information foundations. The project's derivations and cited primary papers supply the specialized locality, estimation and approximation results; those citations are proof support, not additional educational anchors.

## Background/preliminaries: M01–M11

<a id="m01"></a>
### M01: A local observable and its measurable signal

**Central question:** What can a single Pauli measurement reveal about a qubit?

**Understanding target:** Distinguish a state, a Hermitian observable, its possible measurement outcomes and its expectation. Relate a small unitary rotation to a change in an observable's mean, while recognizing that one outcome does not determine that mean.

**Dependencies and story role:** None. This supplies the smallest physical object used throughout the project.

**Conceptual connection:** The final learner extracts many coefficients through carefully chosen one-site output signals.

**Sources:** [N&C §§2.1.3, 2.2.3–2.2.5][nc-ch2]; [reading one local coefficient](../science/local_response.md#4-reading-one-local-coefficient).

<a id="m02"></a>
### M02: Pauli strings and local interactions

**Central question:** How does a list of small interactions describe a large quantum system?

**Understanding target:** Interpret tensor-product Pauli strings, their support and weight, and their real Hamiltonian coefficients. Distinguish an interaction's locality from the dimension of the full state space; explain why the identity coefficient is unobservable here.

**Dependencies and story role:** M01. Extends one-qubit observables to the many-body objects that the algorithm learns.

**Conceptual connection:** Known bounded-support strings provide a compact physical output even though the propagator acts on an exponentially large space.

**Sources:** [N&C §§2.1.7, 2.2.7–2.2.8][nc-ch2]; [Hamiltonian family](../science/model.md#1-hamiltonian-family).

<a id="m03"></a>
### M03: Evolution along a waveform

**Central question:** Why does the order of Hamiltonians during a pulse matter?

**Understanding target:** Relate a time-dependent generator to its propagator and distinguish a prefix from the completed pulse. Explain why exponentiating an integrated Hamiltonian is generally insufficient when generators at different times do not commute.

**Dependencies and story role:** M01–M02. Introduces the dynamical object queried by the experiment.

**Conceptual connection:** Waveform learning concerns the generator at every time, which contains information beyond a final unitary.

**Sources:** [N&C §§2.1.8–2.1.9, 2.2.2][nc-ch2]; [model and propagator conventions](../science/model.md#1-hamiltonian-family); [endpoint ambiguity](../science/interpretation.md#identical-final-gates-can-hide-different-noncommuting-waveforms).

<a id="m04"></a>
### M04: Traces, mixtures and local information

**Central question:** How can a local quantity be extracted without describing every amplitude?

**Understanding target:** Interpret density operators, expectation traces and reduced states. Recognize normalized Pauli traces as coefficient selectors, and distinguish discarding an environment from formally averaging away exterior operator components.

**Dependencies and story role:** M02. Establishes the representation used for both measured transfer data and locality proofs.

**Conceptual connection:** The normalized partial trace later constructs local approximations to a dressed interaction; it is a mathematical decomposition, not an extra experimental operation.

**Sources:** [N&C §§2.4.1–2.4.3][nc-ch2]; [local interaction moments](../science/local_response.md#2-local-interaction-moments).

<a id="m05"></a>
### M05: A channel experiment with product probes

**Central question:** What does an input/output Pauli correlation say about an unknown evolution?

**Understanding target:** View a circuit as a map from prepared states to outcome distributions. Relate product input choices and local output measurements to process-transfer entries, without assuming that intermediate states remain unentangled.

**Dependencies and story role:** M03–M04. Connects the operator description to the actual laboratory data.

**Conceptual connection:** Each complete shot starts and ends locally, while coherent dynamics inside that shot can be many-body.

**Sources:** [N&C §§8.2.1–8.2.3][nc-ch8], [§8.4.2][nc-ch9]; [operational access](../science/model.md#3-operational-access).

<a id="m06"></a>
### M06: Estimation from shared random data

**Central question:** How can finitely many noisy outcomes support simultaneous coefficient estimates?

**Understanding target:** Distinguish expectation, variance, systematic bias and failure probability. Explain why shared data can estimate many observables and why a union bound does not require those estimates to be independent.

**Dependencies and story role:** M05. Adds the statistical layer required for a finite-confidence learning claim.

**Conceptual connection:** Local estimator variance and logarithmic confidence overhead determine shot cost; they do not remove the work of preparing and reading all qubits.

**Sources:** [N&C Appendix 1][nc-appendices]; [product-state estimator and concentration](../science/local_response.md#5-product-state-transfer-estimator).

<a id="m07"></a>
### M07: Accuracy has an operational meaning

**Central question:** Which notion of error does this learning task promise?

**Understanding target:** Separate uniform coefficient-function error, state distinguishability and global channel error. Explain how small errors in each of many local terms can coexist with a large global operator difference.

**Dependencies and story role:** M04, M06. Establishes the metric distinctions needed to interpret the theorem and its comparison algorithms.

**Conceptual connection:** N&C's distance measures motivate operational error control; the project's local metric and diamond-norm implementation bounds require their own arguments.

**Sources:** [N&C §§9.2.1–9.2.3, 9.3][nc-ch9]; [output and error](../science/model.md#2-output-and-error).

<a id="m08"></a>
### M08: Known controls and unknown access

**Central question:** Which operations does a classical description actually make available?

**Understanding target:** Distinguish an unknown forward query from a compiled known inverse and a controlled unknown query. Account for gate accuracy, ancillary workspace and execution when a known unitary is implemented.

**Dependencies and story role:** M03, M07. Defines the operational resources before any amplification argument.

**Conceptual connection:** Coherent replay requires calibrated controls on the same register and a restartable drive clock; an explicit matrix description alone is insufficient.

**Sources:** [N&C §§4.3, 4.5.3–4.6][nc-ch4]; [operational access](../science/model.md#3-operational-access); [inverse compilation](../science/resources.md#compiling-the-known-inverse).

<a id="m09"></a>
### M09: Geometry, local strength and simulation

**Central question:** What prevents a many-body control problem from automatically costing exponentially much?

**Understanding target:** Identify the distinct assumptions of bounded support, bounded incidence, finite range and fixed-dimensional geometry. Relate local Hamiltonian structure to simulation cost while keeping the total norm separate from the strength seen near one site.

**Dependencies and story role:** M02–M03, M08. Builds the spatial framework for the project's local proof.

**Conceptual connection:** Fixed-time locality controls how far a local residual spreads; geometric simulation separately supplies a paid implementation of known controls.

**Sources:** [N&C §§4.7.1–4.7.4][nc-ch4]; [model assumptions](../science/model.md#1-hamiltonian-family); [local interaction moments](../science/local_response.md#2-local-interaction-moments).

<a id="m10"></a>
### M10: A finite waveform model with stable accuracy

**Central question:** What does the polynomial promise contribute beyond a compact notation?

**Understanding target:** Distinguish function accuracy from accuracy of coordinates in a chosen polynomial basis. Explain why fixed degree controls derivative growth, interpolation conditioning and classical output length, and why degree depending on precision changes a complexity claim.

**Dependencies and story role:** M06, M09. Adds the temporal structure required for stable reconstruction.

**Conceptual connection:** The parameter class connects physical regularity to a finite classical output; its specialized approximation bounds are supplied in the project.

**Sources:** [N&C §3.2.1][nc-ch2]; [output representation](../science/model.md#2-output-and-error); [derivative conditioning](../science/reconstruction.md#1-derivative-conditioning-from-the-polynomial-promise).

<a id="m11"></a>
### M11: Background synthesis: the complete learning experiment

**Central question:** What precisely counts as solving this calibration problem?

**Understanding target:** Assemble the unknown local polynomial generator, available prefix/control operations, random measurements, uniform output guarantee and resource units into one consistent task. Identify which assumptions concern identifiability, coherent access, efficient computation or accuracy.

**Dependencies and story role:** M05, M07–M10. Integrates the background from local objects to the full experimental problem.

**Conceptual connection:** A useful precision law must connect a physical interaction model to accessible data and a charged classical answer.

**Sources:** [N&C §§4.6, 7.2][nc-ch4]; [exact theorem](../science/model.md#4-theorem-coherent-replay-waveform-learning); [resource ledger](../science/resources.md).

## Narrative/innovation: M12–M30

<a id="m12"></a>
### M12: Why prefixes reveal otherwise hidden interactions

**Central question:** Can different noncommuting waveforms implement exactly the same final gate?

**Understanding target:** Explain the time-antisymmetric example: the second half reverses the first, while intermediate prefixes remain informative. Distinguish this exact identifiability argument from the later algorithm's precision advantage.

**Dependencies and story role:** M11. Opens the narrative with the physical information the desired output adds.

**Conceptual connection:** Endpoint calibration remains incomplete for noncommuting, time-ordered dynamics, even when completed-gate tomography is perfect.

**Sources:** [N&C §§2.2.2, 2.2.7][nc-ch2]; [identical final gates](../science/interpretation.md#identical-final-gates-can-hide-different-noncommuting-waveforms).

<a id="m13"></a>
### M13: Arrange the residual echo correctly

**Central question:** How can a current model isolate the unknown discrepancy coherently?

**Understanding target:** Track the execution order in $`E_t=U_H(t)U_{\widehat H}(t)^\dagger`$: the known inverse acts first. Explain why exact agreement gives identity, and why replay retains the register's quantum state while restarting the classical schedule.

**Dependencies and story role:** M08, M12. Establishes the actual operation whose response is analyzed next.

**Conceptual connection:** Learned-inverse amplification is an inherited mechanism used here with prefix-dependent corrections.

**Sources:** [N&C §2.1.6][nc-ch2], [§4.6][nc-ch4]; [right-echo construction](../science/local_response.md#1-an-exact-weak-generator-representation); [HKOT2023 attribution](../references/RELATED_WORK.md#hkot2023).

<a id="m14"></a>
### M14: The exact dressed residual

**Central question:** What generator describes the echo when the two drives do not commute?

**Understanding target:** Follow the interpolating path from identity to the right echo and identify its generator as the residual conjugated by known reference evolution. Distinguish this exact representation from a first-order approximation to its measured effect.

**Dependencies and story role:** M03, M13. Converts an operational construction into an analyzable weak interaction.

**Conceptual connection:** The reference changes the residual's operator support while preserving its perturbative origin.

**Sources:** [N&C §§2.1.8–2.1.9, 2.2.2][nc-ch2]; [exact weak-generator representation](../science/local_response.md#1-an-exact-weak-generator-representation).

<a id="m15"></a>
### M15: Spatial spreading with bounded local moments

**Central question:** Why does dressing a small local residual remain manageable in a large system?

**Understanding target:** Explain the conditional-expectation shell decomposition and the competition between polynomial neighborhood growth and exponential spatial decay. Distinguish local interaction strength $`J_0`$ from the support-weighted moment $`J_1`$.

**Dependencies and story role:** M04, M09, M14. Supplies the size-independent ingredient on which amplification depends.

**Conceptual connection:** A residual may be extensive globally while each site's weighted interaction sum remains proportional to its local error scale.

**Sources:** [N&C §2.4.3][nc-ch2], [§4.7][nc-ch4]; [Lemma 1](../science/local_response.md#2-local-interaction-moments); [NSY2019 proof framework](../references/RELATED_WORK.md#nsy2019).

<a id="m16"></a>
### M16: Control the nonlinear effect of many echoes

**Central question:** What keeps coherent repetition from invalidating the local linear response?

**Understanding target:** Trace the overlap count in a double commutator and its bound by $`J_0J_1`$. Explain how the exact second-order Heisenberg integral yields a remainder proportional to $`(q t\delta)^2`$, with no requirement that $`n\delta`$ be small.

**Dependencies and story role:** M15. Turns spatial locality into a quantitative amplification guarantee.

**Conceptual connection:** The measured observable remains the focus of the error bound, even while the experiment acts on the full register.

**Sources:** [N&C §§2.1.9, 2.2.2][nc-ch2]; [Lemma 2 and its integral proof](../science/local_response.md#3-a-local-dyson-bound-for-arbitrarily-many-repetitions).

<a id="m17"></a>
### M17: Select one response coefficient with Pauli algebra

**Central question:** Which input/output pair exposes a desired coefficient of the integrated response?

**Understanding target:** Relate an anticommuting one-site $`Q`$ and signed Pauli $`B=iPQ`$ to the transfer signal $`2q l_P(t)`$. Track Hermiticity, the Pauli sign and normalized-trace coefficient extraction.

**Dependencies and story role:** M01, M04, M16. Makes the local expansion operationally measurable.

**Conceptual connection:** Choosing the commutator channel converts a many-body coefficient into a one-site output correlation.

**Sources:** [N&C §§2.1.3, 2.1.9][nc-ch2]; [coefficient extraction and sign convention](../science/local_response.md#4-reading-one-local-coefficient).

<a id="m18"></a>
### M18: Estimate all required transfers in parallel

**Central question:** How do random product probes share information across many local coefficients?

**Understanding target:** Explain the input-axis and output-axis matching weights, unbiasedness and the second moment $`3^{w+1}`$. Connect constant Pauli weight to bounded variance and simultaneous estimation of an extensive target set.

**Dependencies and story role:** M05–M06, M17. Provides the finite-shot data primitive for reconstruction.

**Conceptual connection:** Parallel statistical reuse explains the logarithmic size factor in shot count while leaving linear preparation, readout and processing costs visible.

**Sources:** [N&C §8.4.2][nc-ch9], [Appendix 1][nc-appendices]; [process estimator](../science/local_response.md#5-product-state-transfer-estimator); [H2020 attribution](../references/RELATED_WORK.md#h2020).

<a id="m19"></a>
### M19: Recover the instantaneous residual

**Central question:** How does an integrated response determine a noncommuting waveform?

**Understanding target:** Interpret $`R(t)=L_t'+i[\widehat H(t),L_t]`$ as a derivative plus a known rotation correction. Explain why each original coefficient requires only a bounded number of additional Pauli coefficients, of weight at most $`2k-1`$.

**Dependencies and story role:** M14, M17. Converts measured response information into the actual learning target.

**Conceptual connection:** Noncommutativity introduces a computable local correction rather than an unknown global inversion problem.

**Sources:** [N&C §2.1.9][nc-ch2]; [response identity](../science/local_response.md#1-an-exact-weak-generator-representation); [required local data](../science/local_response.md#6-the-local-data-required-for-waveform-inversion).

<a id="m20"></a>
### M20: Condition temporal differentiation locally

**Central question:** Why can differentiation be controlled at the scale of the residual error?

**Understanding target:** Connect the polynomial derivative bound, local overlap counts and response equation to a second-derivative bound proportional to $`(1+m^2)\delta`$. Recognize that the response itself need not be a polynomial.

**Dependencies and story role:** M10, M15, M19. Resolves the stability issue created by the temporal inverse.

**Conceptual connection:** Small residual coefficients and finite temporal complexity jointly control differentiation, independently of global operator-norm error.

**Sources:** [N&C §2.1.9][nc-ch2]; [derivative-conditioning proof](../science/reconstruction.md#1-derivative-conditioning-from-the-polynomial-promise); [polynomial inequality support](../references/RELATED_WORK.md#trefethen2013).

<a id="m21"></a>
### M21: Choose times that remain fixed during refinement

**Central question:** How can finitely many prefixes determine an entire coefficient function?

**Understanding target:** Relate one-sided differences, Chebyshev–Lobatto nodes and interpolation norm to the uniform target. Explain endpoint handling and the degree-zero case, and why spacing depends on degree but not the current accuracy radius.

**Dependencies and story role:** M10, M20. Turns the continuous inverse into a finite experimental schedule.

**Conceptual connection:** Interpolation reconstructs the polynomial residual from approximate nodal values; finite differences only approximate the response derivative.

**Sources:** [N&C §3.2.1][nc-ch2]; [fixed times and scales](../science/reconstruction.md#2-fixed-times-and-explicit-accuracy-scales); [interpolation proof support](../references/RELATED_WORK.md#trefethen2013).

<a id="m22"></a>
### M22: Close one complete contraction

**Central question:** Why does one update improve a certified model despite several different errors?

**Understanding target:** Combine shot error, nonlinear echo bias, implementation error, finite-difference bias, interpolation and arithmetic rounding. Explain the roles of $`q\delta`$, response division by $`2q`$, and the derivative factor $`1/h`$ in obtaining a smaller uniform radius.

**Dependencies and story role:** M18–M19, M21. Integrates the local mechanism into a complete refinement step.

**Conceptual connection:** A precision gain becomes an algorithmic guarantee only after every error reaches the same coefficient-function metric.

**Sources:** [N&C §§9.2.1, 9.3][nc-ch9]; [one refinement step](../science/reconstruction.md#3-one-refinement-step).

<a id="m23"></a>
### M23: Keep controls bounded on every history

**Central question:** What prevents an unlucky statistical update from demanding unbounded controls?

**Understanding target:** Explain why the polynomial guard bounds accepted models between grid points, why successful histories pass it, and why pointwise clipping would invalidate the polynomial class. Separate an accuracy failure from an uncontrolled resource demand.

**Dependencies and story role:** M10, M22. Extends the resource guarantee beyond the favorable statistical event.

**Conceptual connection:** A worst-case algorithmic cost needs controlled behavior even when its probabilistic accuracy guarantee fails.

**Sources:** [N&C §3.2.1][nc-ch2]; [bounded controllers on every history](../science/reconstruction.md#4-bounded-controllers-on-every-history).

<a id="m24"></a>
### M24: Pay for the first accurate model

**Central question:** Where does the model needed to start residual amplification come from?

**Understanding target:** Explain the imported independent-prefix initializer, its inverse-polynomial starting accuracy and its degree dependence. Distinguish an analytic localization region from the constant-size probe optimization problems actually used by that algorithm.

**Dependencies and story role:** M11, M23. Removes the provisional assumption that a good initial model is supplied.

**Conceptual connection:** Coarse learning and coherent refinement solve different precision regimes within one charged workflow.

**Sources:** [N&C §8.4.2][nc-ch9]; [paid initialization](../science/resources.md#paid-initialization); [F2026, Corollary 5.1 and §§6–7](../references/RELATED_WORK.md#f2026).

<a id="m25"></a>
### M25: Assemble adaptive stages and global confidence

**Central question:** How do local refinements produce a trustworthy final answer at inverse-precision cost?

**Understanding target:** Follow the induction over halved radii, conditional concentration for adaptively selected circuits and the failure-budget sum. Explain why geometrically increasing repetitions sum to order $`1/\epsilon`$, while fresh-shot count grows differently.

**Dependencies and story role:** M22–M24. Integrates initialization and refinement into the full statistical algorithm.

**Conceptual connection:** Fresh data make each stage's conditional guarantee usable without enumerating every possible previous model.

**Sources:** [N&C Appendix 1][nc-appendices], [§3.2.1][nc-ch2]; [adaptive confidence](../science/reconstruction.md#6-iteration-and-adaptive-confidence); [refinement count](../science/reconstruction.md#7-refinement-resource-count).

<a id="m26"></a>
### M26: Charge the complete implementation

**Central question:** Does the precision improvement survive paying for known controls and classical output?

**Understanding target:** Account for reversed negative schedule simulation, per-inverse accuracy, repeated executed gates, compilation, preparation, readout, storage and arithmetic. Distinguish logarithmic experimental size dependence from the extensive complete workload.

**Dependencies and story role:** M08–M09, M25. Converts the query result into an implementation resource statement.

**Conceptual connection:** Efficient structure and high-precision simulation preserve the precision exponent while explicit local data supply and output remain charged.

**Sources:** [N&C §§4.5.3, 4.7][nc-ch4]; [inverse compilation](../science/resources.md#compiling-the-known-inverse); [classical costs](../science/resources.md#classical-work-readout-and-storage); [HHKL2020](../references/RELATED_WORK.md#hhkl2020).

<a id="m27"></a>
### M27: Understand the optimality claim and its comparator

**Central question:** What exactly prevents a better precision exponent?

**Understanding target:** Reduce learning to distinguishing two static Pauli amplitudes and follow the hybrid bound in total unknown exposure. Contrast this with fresh, bounded-duration, memory-free shots, whose distinguishability accumulates differently.

**Dependencies and story role:** M07, M25–M26. Places the upper bound against a matched operational lower bound.

**Conceptual connection:** Controls change the available experiment; optimal precision dependence does not imply optimal degree dependence, gate count or wall time.

**Sources:** [N&C §§9.2.1–9.2.2][nc-ch9], [§6.7][nc-ch4]; [precision lower bounds](../science/resources.md#precision-lower-bound).

<a id="m28"></a>
### M28: Locate the physical accuracy and coherence requirements

**Central question:** Which imperfections eventually prevent further useful replay?

**Understanding target:** Distinguish grid spacing from clock accuracy, gate-synthesis precision from physical gate error, and calibrated readout bias from noise within the sequence. Explain why fixed per-pair decoherence or drift can defeat ever-longer coherent amplification.

**Dependencies and story role:** M07–M08, M26. Identifies the physical conditions under which the resource law applies.

**Conceptual connection:** Error budgets shrinking with the residual are implementation requirements; fault-tolerant known controls alone do not correct an unknown noisy signal.

**Sources:** [N&C §8.3.6][nc-ch8], [§10.6.1][nc-ch9]; [implementation accuracy and noise](../science/resources.md#implementation-accuracy-and-noise).

<a id="m29"></a>
### M29: Interpret the finite-shot evidence

**Central question:** What does the two-qubit calculation establish about the general algorithm?

**Understanding target:** Connect the noncommuting example, sign and ordering checks, multinomial product-probe data and recovered uniform errors to the analytic mechanism. Separate numerical observations from the theorem, and include the example's large physical shot and prefix counts.

**Dependencies and story role:** M12, M22, M25, M28. Brings the complete construction into contact with reproducible finite data.

**Conceptual connection:** Exact small-system simulation can test implementation and bias while neither proving large-system performance nor establishing a practical crossover.

**Sources:** [N&C §8.4.2][nc-ch9], [Appendix 1][nc-appendices]; [finite-shot results and actual cost](../verification/README.md#finite-shot-results-and-the-actual-cost); [interpretation](../science/interpretation.md#a-finite-shot-two-qubit-reconstruction).

<a id="m30"></a>
### M30: Narrative synthesis: the contribution as a whole

**Central question:** When does coherent replay provide a useful answer to full pulse calibration?

**Understanding target:** Connect prefix identifiability, inherited amplification, the local remainder and differential inverse, stable reconstruction and paid resources into one explanation. State the precise output, access assumptions, proven precision gain and physical limitations, distinguishing them from a universal classical speedup or demonstrated hardware advantage.

**Dependencies and story role:** M26–M29, integrating M12–M25. Completes the narrative from a local response signal to the scientific result and its scope.

**Conceptual connection:** The value is time-resolved local interaction knowledge under a scalable coherent experimental model, with the limits needed to assess its use.

**Sources:** [N&C §3.2.1][nc-ch2], [§7.2][nc-ch4]; [contribution and boundary](../science/model.md#5-contribution-and-boundary); [implementation comparison](../science/interpretation.md#a-meaningful-implementation-comparison); [related work](../references/RELATED_WORK.md).

[nc-contents]: https://assets.cambridge.org/97811070/02173/frontmatter/9781107002173_frontmatter.pdf
[nc-ch2]: https://assets.cambridge.org/97811070/02173/frontmatter/9781107002173_frontmatter.pdf#page=8
[nc-ch4]: https://assets.cambridge.org/97811070/02173/frontmatter/9781107002173_frontmatter.pdf#page=9
[nc-ch8]: https://assets.cambridge.org/97811070/02173/frontmatter/9781107002173_frontmatter.pdf#page=10
[nc-ch9]: https://assets.cambridge.org/97811070/02173/frontmatter/9781107002173_frontmatter.pdf#page=11
[nc-appendices]: https://assets.cambridge.org/97811070/02173/frontmatter/9781107002173_frontmatter.pdf#page=12
