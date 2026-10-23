"""Small-system checks of coherent replay waveform learning.

This is a dense, two-qubit numerical experiment, not a proof, device benchmark,
noise-robustness claim, or large-system simulation algorithm.  Random outcomes
are drawn from the exact multinomial distribution of product-Pauli experiments.

Run from the repository root:
    python3 verification/verify_protocol.py --output verification/generated/protocol.json
Recorded environment: Python 3.12.14; dependencies are pinned in
verification/requirements.txt.
"""

from __future__ import annotations

import argparse
from itertools import product
import json
from pathlib import Path
import platform
import time

import numpy as np
import scipy
from scipy.integrate import solve_ivp


N_QUBITS = 2
DIM = 2**N_QUBITS
DEGREE = 3
IDENTITY = np.eye(DIM, dtype=complex)
SINGLE = {
    "I": np.eye(2, dtype=complex),
    "X": np.array([[0, 1], [1, 0]], dtype=complex),
    "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
    "Z": np.diag([1, -1]).astype(complex),
}


def pauli(word: str) -> np.ndarray:
    out = np.ones((1, 1), dtype=complex)
    for char in word:
        out = np.kron(out, SINGLE[char])
    return out


WORDS = ["".join(word) for word in product("IXYZ", repeat=N_QUBITS)]
BASIS = {word: pauli(word) for word in WORDS}
NONIDENTITY = [word for word in WORDS if word != "I" * N_QUBITS]
MATRICES = np.array([BASIS[word] for word in NONIDENTITY])
MODEL_WORDS = ["XI", "ZZ", "IZ", "IX", "YY"]
MODEL_MATRICES = np.array([BASIS[word] for word in MODEL_WORDS])
NODES = np.array([0.0, 0.25, 0.75, 1.0])
FD_H = 0.125
INITIAL_BOUND = 0.05
TAU = 0.10


def coefficient(matrix: np.ndarray, word: str) -> float:
    return float(np.trace(BASIS[word] @ matrix).real / DIM)


def schedule_coefficients() -> tuple[np.ndarray, np.ndarray]:
    """Chebyshev coefficients on x=2t-1 for nominal and unknown schedules.

    Every nonzero term is odd in x, so both schedules obey H(1-t)=-H(t)
    and have exactly the same endpoint U(1)=I.  Different times do not commute.
    """
    nominal = np.zeros((len(MODEL_WORDS), DEGREE + 1))
    nominal[0, 1] = 0.25
    nominal[1, 1] = 0.20
    nominal[2, 1] = 0.15
    nominal[3, [1, 3]] = [0.18 * 0.75, 0.18 * 0.25]
    nominal[4, [1, 3]] = [0.12 * 0.75, 0.12 * 0.25]
    residual = np.zeros_like(nominal)
    # 0.60x+0.25x^3, -0.40x+0.35x^3, and 0.30x-0.20x^3.
    residual[0, [1, 3]] = [0.60 + 0.25 * 0.75, 0.25 * 0.25]
    residual[1, [1, 3]] = [-0.40 + 0.35 * 0.75, 0.35 * 0.25]
    residual[3, [1, 3]] = [0.30 - 0.20 * 0.75, -0.20 * 0.25]
    return nominal, residual


def values(coeffs: np.ndarray, times: np.ndarray | float) -> np.ndarray:
    x = 2 * np.asarray(times) - 1
    return np.polynomial.chebyshev.chebval(x, coeffs.T)


def hamiltonian(coeffs: np.ndarray, t: float) -> np.ndarray:
    return np.einsum("a,aij->ij", values(coeffs, t), MODEL_MATRICES)


def propagate(coeffs: np.ndarray):
    def rhs(t, flattened):
        unitary = flattened.reshape(DIM, DIM)
        return (-1j * hamiltonian(coeffs, t) @ unitary).ravel()

    solution = solve_ivp(
        rhs,
        (0.0, 1.0),
        IDENTITY.ravel(),
        method="DOP853",
        rtol=2e-12,
        atol=2e-14,
        dense_output=True,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    return lambda t: solution.sol(t).reshape(DIM, DIM)


def response_by_quadrature(model, residual_coeffs, t, order=64):
    nodes, weights = np.polynomial.legendre.leggauss(order)
    final_u = model(t)
    response = np.zeros((DIM, DIM), dtype=complex)
    for node, weight in zip(nodes, weights):
        s = t * (node + 1) / 2
        segment = final_u @ model(s).conj().T
        response += weight * segment @ hamiltonian(residual_coeffs, s) @ segment.conj().T
    return t * response / 2


def probe_for(word):
    site = next(i for i, char in enumerate(word) if char != "I")
    out_word = ["I"] * N_QUBITS
    out_word[site] = {"X": "Y", "Y": "Z", "Z": "X"}[word[site]]
    out_word = "".join(out_word)
    input_matrix = 1j * BASIS[word] @ BASIS[out_word]
    input_word = max(WORDS, key=lambda w: abs(coefficient(input_matrix, w)))
    sign = int(round(coefficient(input_matrix, input_word)))
    assert np.linalg.norm(input_matrix - sign * BASIS[input_word]) < 1e-12
    return input_word, sign, out_word


PROBES = [probe_for(word) for word in NONIDENTITY]


class ProductProcessShadows:
    """Enumerate exact outcome probabilities, then sample multinomial counts.

    The finite outcome space is only used by this classical verifier.  A real
    shot independently chooses input axes/signs and output axes, prepares the
    product eigenstate, applies the echo circuit, and measures product Paulis.
    """

    def __init__(self):
        self.axes = []
        self.signs = []
        states = []
        for axes in product("XYZ", repeat=N_QUBITS):
            for signs in product((-1, 1), repeat=N_QUBITS):
                state = np.ones(1, dtype=complex)
                for axis, sign in zip(axes, signs):
                    eigenvalues, eigenvectors = np.linalg.eigh(SINGLE[axis])
                    local = eigenvectors[:, np.argmin(abs(eigenvalues - sign))]
                    state = np.kron(state, local)
                self.axes.append(axes)
                self.signs.append(signs)
                states.append(state)
        self.states = np.array(states).T
        self.axes = np.array(self.axes)
        self.signs = np.array(self.signs)
        weights = []
        for input_word, input_sign, output_word in PROBES:
            input_weight = self.pauli_weight(input_word) * input_sign
            output_weight = self.pauli_weight(output_word)
            weights.append(np.outer(input_weight, output_weight).ravel())
        self.weights = np.array(weights)

    def pauli_weight(self, word):
        result = np.ones(len(self.axes))
        for site, char in enumerate(word):
            if char != "I":
                result *= 3 * (self.axes[:, site] == char) * self.signs[:, site]
        return result

    def probabilities(self, unitary):
        amplitudes = self.states.conj().T @ unitary @ self.states
        probabilities = (abs(amplitudes) ** 2).T / (len(self.axes) * 3**N_QUBITS)
        probabilities = probabilities.ravel()
        # Remove O(ODE tolerance) normalization drift, not physical shot noise.
        return probabilities / probabilities.sum()

    def exact_transfers(self, unitary):
        return self.weights @ self.probabilities(unitary)

    def sample(self, unitary, shots, rng):
        probabilities = self.probabilities(unitary)
        counts = rng.multinomial(shots, probabilities)
        estimates = self.weights @ counts / shots
        means = self.weights @ probabilities
        variance = self.weights**2 @ probabilities - means**2
        return estimates, np.sqrt(np.maximum(variance, 0) / shots)


def direct_transfers(unitary):
    return np.array(
        [
            coefficient(unitary @ (sign * BASIS[bin_word]) @ unitary.conj().T, q_word)
            for bin_word, sign, q_word in PROBES
        ]
    )


def algebra_checks(shadows):
    nominal, shape = schedule_coefficients()
    residual = INITIAL_BOUND * shape
    model = propagate(nominal)
    true = propagate(nominal + residual)
    t = 0.63
    ell = response_by_quadrature(model, residual, t)
    h = 2e-5
    ell_prime = (
        response_by_quadrature(model, residual, t + h)
        - response_by_quadrature(model, residual, t - h)
    ) / (2 * h)
    hh = hamiltonian(nominal, t)
    recovered = ell_prime + 1j * (hh @ ell - ell @ hh)
    rr = hamiltonian(residual, t)

    # Integrate the exact right-echo residual schedule independently.
    end_model = model(t)

    def rhs_g(s, flattened):
        segment = end_model @ model(s).conj().T
        g = segment @ hamiltonian(residual, s) @ segment.conj().T
        return (-1j * g @ flattened.reshape(DIM, DIM)).ravel()

    g_solution = solve_ivp(rhs_g, (0, t), IDENTITY.ravel(), method="DOP853", rtol=2e-12, atol=2e-14)
    residual_unitary = g_solution.y[:, -1].reshape(DIM, DIM)
    right_echo = true(t) @ model(t).conj().T
    left_echo = model(t).conj().T @ true(t)

    lam = 1e-4
    plus = propagate(nominal + lam * residual)
    minus = propagate(nominal - lam * residual)
    finite_response = 1j * (plus(t) - minus(t)) @ model(t).conj().T / (2 * lam)

    # Verify the shadow estimator against direct matrix traces and its variance bound.
    amplified = np.linalg.matrix_power(right_echo, 5)
    probabilities = shadows.probabilities(amplified)
    second_moment = shadows.weights**2 @ probabilities
    bounds = np.array([3 ** (sum(ch != "I" for ch in w) + 1) for w, _, _ in PROBES])

    local_rows = []
    for delta in [0.08, 0.04, 0.02, 0.01, 0.005]:
        ut = propagate(nominal + delta * shape)
        e = ut(t) @ model(t).conj().T
        l = response_by_quadrature(model, delta * shape, t)
        observed = direct_transfers(e)
        linear = 2 * np.array([coefficient(l, word) for word in NONIDENTITY])
        error = float(np.max(abs(observed - linear)))
        local_rows.append({"delta": delta, "q": 1, "max_transfer_remainder": error, "remainder_over_delta_squared": error / delta**2})

    return {
        "prefix": t,
        "response_differential_identity_operator_error": float(np.linalg.norm(recovered - rr, 2)),
        "response_differential_identity_relative_error": float(np.linalg.norm(recovered - rr, 2) / np.linalg.norm(rr, 2)),
        "right_echo_vs_exact_residual_evolution": float(np.linalg.norm(right_echo - residual_unitary, 2)),
        "wrong_left_echo_vs_same_residual_evolution": float(np.linalg.norm(left_echo - residual_unitary, 2)),
        "quadrature_vs_symmetric_parameter_derivative": float(np.linalg.norm(ell - finite_response, 2)),
        "shadow_mean_vs_direct_transfer_max_error": float(np.max(abs(shadows.exact_transfers(amplified) - direct_transfers(amplified)))),
        "max_shadow_second_moment_over_proved_bound": float(np.max(second_moment / bounds)),
        "local_linear_response_remainder": local_rows,
    }


def stencils():
    output = []
    for node in NODES:
        if node == 0:
            output.append([(0.0, -3 / (2 * FD_H)), (FD_H, 4 / (2 * FD_H)), (2 * FD_H, -1 / (2 * FD_H))])
        elif node == 1:
            output.append([(1.0, 3 / (2 * FD_H)), (1 - FD_H, -4 / (2 * FD_H)), (1 - 2 * FD_H, 1 / (2 * FD_H))])
        else:
            output.append([(node - FD_H, -1 / (2 * FD_H)), (node + FD_H, 1 / (2 * FD_H))])
    return output


STENCILS = stencils()
PREFIXES = sorted(set(NODES) | {t for stencil in STENCILS for t, _ in stencil})


def waveform_error(estimate, truth, grid=None):
    """Maximize each cubic error over endpoints and real derivative roots.

    This removes discretization error from a plotting grid.  Root finding is
    floating-point, so it is not a formally interval-certified upper bound.
    """
    errors = []
    for polynomial in estimate - truth:
        derivative = np.polynomial.chebyshev.chebder(polynomial)
        roots = np.polynomial.chebyshev.chebroots(derivative)
        candidates = [-1.0, 1.0]
        candidates.extend(float(root.real) for root in roots if abs(root.imag) < 1e-10 and -1 <= root.real <= 1)
        errors.append(float(np.max(abs(np.polynomial.chebyshev.chebval(candidates, polynomial)))))
    errors = np.array(errors)
    return float(np.max(errors)), {word: float(err) for word, err in zip(MODEL_WORDS, errors)}


def refinement(estimate, truth, true_propagator, bound, shadows, shots, rng):
    model = propagate(estimate)
    q = max(1, int(round(TAU / bound)))
    estimates = {0.0: np.zeros((DIM, DIM), complex)}
    max_transfer_se = 0.0
    for t in PREFIXES:
        if t == 0:
            continue
        echo = true_propagator(t) @ model(t).conj().T
        amplified = np.linalg.matrix_power(echo, q)
        if shots == 0:
            transfers = shadows.exact_transfers(amplified)
        else:
            transfers, se = shadows.sample(amplified, shots, rng)
            max_transfer_se = max(max_transfer_se, float(np.max(se)))
        estimates[t] = np.einsum("a,aij->ij", transfers / (2 * q), MATRICES)

    residual_values = np.zeros((len(MODEL_WORDS), len(NODES)))
    for i, (node, stencil) in enumerate(zip(NODES, STENCILS)):
        derivative = sum(weight * estimates[t] for t, weight in stencil)
        hh = hamiltonian(estimate, node)
        recovered = derivative + 1j * (hh @ estimates[node] - estimates[node] @ hh)
        residual_values[:, i] = [coefficient(recovered, word) for word in MODEL_WORDS]
    correction = np.polynomial.chebyshev.chebfit(2 * NODES - 1, residual_values.T, DEGREE).T
    return estimate + correction, {
        "q": q,
        "maintained_input_bound": bound,
        "max_exact_transfer_standard_error": max_transfer_se,
        "shots_per_nonzero_prefix": shots,
        "fresh_preparations": shots * (len(PREFIXES) - 1),
        "unknown_prefix_queries": shots * q * (len(PREFIXES) - 1),
        "unknown_evolution_time": float(shots * q * sum(PREFIXES)),
        "known_inverse_total_target_simulation_time": float(shots * q * sum(PREFIXES)),
    }


def learner_trial(shadows, shots, stages, seed, keep_coefficients=False):
    nominal, shape = schedule_coefficients()
    truth = nominal + INITIAL_BOUND * shape
    true = propagate(truth)
    estimate = nominal.copy()
    rng = np.random.default_rng(seed)
    grid = np.linspace(0, 1, 2001)
    start_error, _ = waveform_error(estimate, truth, grid)
    history = []
    all_contract = True
    previous_error = start_error
    for stage in range(stages):
        bound = INITIAL_BOUND / 2**stage
        estimate, metadata = refinement(estimate, truth, true, bound, shadows, shots, rng)
        error, per_term = waveform_error(estimate, truth, grid)
        output_bound = bound / 2
        within = error <= output_bound
        all_contract = all_contract and within
        metadata.update({
            "stage": stage,
            "output_bound": output_bound,
            "uniform_waveform_error": error,
            "error_over_input_bound": error / bound,
            "error_over_previous_actual_error": error / previous_error,
            "within_next_bound": within,
            "per_term_error": per_term,
        })
        history.append(metadata)
        previous_error = error
    final_model = propagate(estimate)
    result = {
        "seed": seed,
        "initial_uniform_error": start_error,
        "all_stages_within_maintained_bounds": all_contract,
        "final_uniform_error": history[-1]["uniform_waveform_error"],
        "learned_endpoint_operator_error": float(np.linalg.norm(final_model(1) - true(1), 2)),
        "history": history,
        "total_fresh_preparations": sum(row["fresh_preparations"] for row in history),
        "total_unknown_prefix_queries": sum(row["unknown_prefix_queries"] for row in history),
        "total_unknown_evolution_time": sum(row["unknown_evolution_time"] for row in history),
        "total_known_inverse_target_simulation_time": sum(row["known_inverse_total_target_simulation_time"] for row in history),
        "maximum_coherent_echo_count": history[-1]["q"],
    }
    if keep_coefficients:
        result["truth_chebyshev_coefficients"] = truth.tolist()
        result["initial_chebyshev_coefficients"] = nominal.tolist()
        result["learned_chebyshev_coefficients"] = estimate.tolist()
        sample_times = np.linspace(0, 1, 21)
        result["waveform_samples"] = {
            "times": sample_times.tolist(),
            "truth": values(truth, sample_times).tolist(),
            "initial": values(nominal, sample_times).tolist(),
            "learned": values(estimate, sample_times).tolist(),
        }
    return result


def endpoint_example(shadows):
    nominal, shape = schedule_coefficients()
    truth = nominal + INITIAL_BOUND * shape
    model, true = propagate(nominal), propagate(truth)
    endpoint_difference = float(np.linalg.norm(true(1) - model(1), 2))
    prefixes = np.linspace(0, 1, 101)
    differences = [np.linalg.norm(true(t) - model(t), 2) for t in prefixes]
    t = 0.375
    echo = true(t) @ model(t).conj().T
    transfers = direct_transfers(echo)
    best = int(np.argmax(abs(transfers)))
    return {
        "exact_argument": "H(1-t)=-H(t) implies that the second half retraces the first half in inverse time order, so U(1)=I. Both nominal and unknown schedules satisfy this identity.",
        "noncommuting_hamiltonian_times": [0.10, 0.35],
        "commutator_operator_norm": float(np.linalg.norm(hamiltonian(truth, 0.10) @ hamiltonian(truth, 0.35) - hamiltonian(truth, 0.35) @ hamiltonian(truth, 0.10), 2)),
        "nominal_endpoint_distance_from_identity": float(np.linalg.norm(model(1) - IDENTITY, 2)),
        "unknown_endpoint_distance_from_identity": float(np.linalg.norm(true(1) - IDENTITY, 2)),
        "endpoint_operator_difference": endpoint_difference,
        "max_sampled_prefix_operator_difference": float(np.max(differences)),
        "max_sampled_prefix_time": float(prefixes[np.argmax(differences)]),
        "uniform_coefficient_difference": waveform_error(nominal, truth, np.linspace(0, 1, 2001))[0],
        "example_prefix": t,
        "example_observable_coefficient": NONIDENTITY[best],
        "example_signed_input_pauli": {"word": PROBES[best][0], "sign": PROBES[best][1]},
        "example_output_pauli": PROBES[best][2],
        "example_unamplified_transfer": float(transfers[best]),
        "endpoint_identifiability": "No endpoint-only experiment, even with perfect tomography or repetitions, can distinguish this pair. This elementary nonidentifiability example is not a novelty claim.",
    }


def fisher_diagnostic(shadows):
    """One-dimensional, matched-echo Fisher information, not an optimal baseline."""
    nominal, shape = schedule_coefficients()
    center = 0.002
    step = 1e-5
    t = 0.375
    model = propagate(nominal)
    mid = propagate(nominal + center * shape)
    plus = propagate(nominal + (center + step) * shape)
    minus = propagate(nominal + (center - step) * shape)
    echoes = [u(t) @ model(t).conj().T for u in [mid, plus, minus]]
    output = []
    first = None
    for q in [1, 2, 4, 8, 16, 32, 64]:
        p, p_plus, p_minus = [shadows.probabilities(np.linalg.matrix_power(e, q)) for e in echoes]
        derivative = (p_plus - p_minus) / (2 * step)
        support = p > 1e-16
        fi = float(np.sum(derivative[support] ** 2 / p[support]))
        if first is None:
            first = fi
        output.append({"q": q, "classical_fisher_information_per_product_shadow_shot": fi, "information_over_q_squared_times_q1": fi / (q**2 * first), "information_per_unknown_time_relative_to_q1": fi / (q * first)})
    return {
        "scope": "Single residual-amplitude family at one fixed prefix; compares identical product process measurements on q-fold echoes versus independent q=1 echoes. Does not optimize the independent-prefix protocol, include control synthesis, or establish a practical crossover.",
        "prefix": t,
        "residual_amplitude": center,
        "derivative_step": step,
        "rows": output,
    }


def controller_bias_diagnostic():
    """Exact single-prefix test of one systematic per-pair control rotation.

    The implemented pair is E_b=E exp(-i b ZI), so the error rotation acts
    immediately before the nominal known inverse.  This is not a stochastic
    noise model or a full noisy waveform-learning benchmark.
    """
    nominal, shape = schedule_coefficients()
    model = propagate(nominal)
    prefix = 0.375
    fixed_b = 2e-4
    proportionality = fixed_b / INITIAL_BOUND
    rows = []
    for stage in range(10):
        delta = INITIAL_BOUND / 2**stage
        q = int(round(TAU / delta))
        true = propagate(nominal + delta * shape)
        echo = true(prefix) @ model(prefix).conj().T
        ideal = direct_transfers(np.linalg.matrix_power(echo, q)) / (2 * q)
        row = {"delta": delta, "q": q}
        for name, b in [("fixed", fixed_b), ("scaled", proportionality * delta)]:
            rotation = np.cos(b) * IDENTITY - 1j * np.sin(b) * BASIS["ZI"]
            implemented = np.linalg.matrix_power(echo @ rotation, q)
            inferred = direct_transfers(implemented) / (2 * q)
            bias = float(np.max(abs(inferred - ideal)))
            row[name + "_rotation_angle"] = b
            row[name + "_max_response_coefficient_bias"] = bias
            row[name + "_bias_over_delta"] = bias / delta
        rows.append(row)
    return {
        "scope": "Exact, noiseless expectation values at one prefix with a systematic per-pair known-controller unitary error. Measures the added bias in inferred response coefficients; does not claim a full noisy waveform guarantee.",
        "prefix": prefix,
        "implemented_pair": "E_t exp(-i b ZI), with the rightmost error rotation acting before the nominal inverse.",
        "fixed_angle": fixed_b,
        "scaled_angle_rule": "b=(fixed_angle/initial_bound)*delta",
        "rows": rows,
        "interpretation": "A fixed per-pair error produces an approximately fixed response-coefficient bias, whose ratio to the shrinking residual grows. Scaling the controller error with delta keeps that relative bias small in this example. This is not noise robustness.",
    }


def run(args):
    start = time.perf_counter()
    shadows = ProductProcessShadows()
    checks = algebra_checks(shadows)
    if checks["right_echo_vs_exact_residual_evolution"] > 1e-8:
        raise AssertionError("Right echo residual identity failed")
    if checks["response_differential_identity_relative_error"] > 1e-5:
        raise AssertionError("Waveform response identity failed")
    if checks["shadow_mean_vs_direct_transfer_max_error"] > 1e-10:
        raise AssertionError("Product process shadow orientation/normalization failed")
    if checks["max_shadow_second_moment_over_proved_bound"] > 1 + 1e-9:
        raise AssertionError("Shadow variance bound failed")

    finite = learner_trial(shadows, args.shots, args.stages, args.seed, keep_coefficients=True)
    noiseless = learner_trial(shadows, 0, args.stages, args.seed)
    trials = [finite]
    for trial in range(1, args.trials):
        trials.append(learner_trial(shadows, args.shots, args.stages, args.seed + trial))
    final_errors = np.array([trial["final_uniform_error"] for trial in trials])
    shot_sweep = []
    for shots in [100_000, 1_000_000, args.shots]:
        sample = learner_trial(shadows, shots, args.stages, args.seed + 100)
        shot_sweep.append({"shots_per_prefix_per_stage": shots, "all_stage_bounds_held": sample["all_stages_within_maintained_bounds"], "final_error": sample["final_uniform_error"], "error_over_final_target_bound": sample["final_uniform_error"] / (INITIAL_BOUND / 2**args.stages)})
    output = {
        "scope": "Finite dense two-qubit verification of the echo orientation, local response, finite-shot process estimator and waveform reconstruction. Numerical checks are not proofs. No noisy-channel or control-error robustness is established.",
        "environment": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
        "configuration": {"seed": args.seed, "shots_per_nonzero_prefix_per_stage": args.shots, "stages": args.stages, "trials": args.trials, "qubits": N_QUBITS, "degree": DEGREE, "model_paulis": MODEL_WORDS, "initial_bound": INITIAL_BOUND, "tau": TAU, "finite_difference_h": FD_H, "chebyshev_lobatto_nodes": NODES.tolist(), "queried_prefixes": PREFIXES, "uniform_error_evaluation": "Endpoints and real roots of the cubic-error derivative; floating-point, not interval-certified."},
        "algebra_checks": checks,
        "endpoint_degenerate_noncommuting_example": endpoint_example(shadows),
        "finite_shot_example": finite,
        "noiseless_same_stencil_example": noiseless,
        "finite_shot_repetition_summary": {"count": len(trials), "all_stage_bound_successes": sum(trial["all_stages_within_maintained_bounds"] for trial in trials), "final_error_min": float(final_errors.min()), "final_error_median": float(np.median(final_errors)), "final_error_max": float(final_errors.max()), "final_errors": final_errors.tolist(), "stage_errors_by_trial": [[row["uniform_waveform_error"] for row in trial["history"]] for trial in trials], "seeds": [trial["seed"] for trial in trials], "interpretation": "Empirical fixed-seed success frequency only; no confidence guarantee or replacement for the theorem."},
        "shot_budget_sweep": shot_sweep,
        "matched_echo_fisher_diagnostic": fisher_diagnostic(shadows),
        "systematic_controller_bias_diagnostic": controller_bias_diagnostic(),
        "unpaid_or_excluded_resources": ["Dense propagation is used only to generate exact small-system outcome distributions.", "Known inverse controls are exact in this experiment; requested simulation times and invocation counts are recorded, but compiled gate counts and hardware execution times are not simulated.", "The nominal starting model is supplied; this experiment does not implement the coarse initializer.", "The shot counts can be very large and are reported explicitly; multinomial count generation does not reduce the physical experimental cost.", "Main waveform-learning runs assume ideal controls and omit environmental noise, schedule jitter, and SPAM bias; the separate controller-bias diagnostic includes a systematic unitary control error.", "The demonstration learns all 15 nonidentity response coefficients for two qubits, rather than optimizing the constant-support coefficient subset.", "Uniform cubic errors are maximized using floating-point derivative roots; the code does not implement interval-certified polynomial maxima."],
    }
    output["runtime_seconds"] = time.perf_counter() - start
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"output": str(path), "runtime_seconds": output["runtime_seconds"], "algebra_checks": checks, "endpoint_example": output["endpoint_degenerate_noncommuting_example"], "finite_shot_repetition_summary": output["finite_shot_repetition_summary"], "finite_shot_history": [{k: row[k] for k in ["stage", "q", "uniform_waveform_error", "error_over_input_bound", "within_next_bound"]} for row in finite["history"]], "shot_budget_sweep": shot_sweep, "fresh_preparations": finite["total_fresh_preparations"], "unknown_evolution_time": finite["total_unknown_evolution_time"]}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=20261023)
    parser.add_argument("--shots", type=int, default=20_000_000)
    parser.add_argument("--stages", type=int, default=6)
    parser.add_argument("--trials", type=int, default=12)
    parser.add_argument("--output", default=str(Path(__file__).with_name("generated") / "protocol.json"))
    run(parser.parse_args())
