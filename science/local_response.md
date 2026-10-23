# Local response from coherent replay

An extensive Hamiltonian can have a small error in every local coefficient while its total operator-norm error grows with the number of qubits. The reconstruction therefore needs a local response estimate whose constants remain independent of system size. This page proves that estimate and gives a product-state experiment for reading the required coefficients.

We use the normalized interval $`[0,1]`$ and the assumptions in [the model](model.md). The reference Hamiltonian $`\widehat H`$ has the same known Pauli interaction pattern as $`H`$. Its coefficients are bounded by $`\bar J=2(J+1)`$; [the reconstruction guard](reconstruction.md#4-bounded-controllers-on-every-history) enforces this on every accepted history. Suppose that the current model satisfies

```math
R(t)=H(t)-\widehat H(t)=\sum_a r_a(t)P_a,
\qquad
\max_a\|r_a\|_{\infty,[0,1]}\le\delta.
```

The repeated learned-inverse echo is an established precision-amplification mechanism; see [HKOT2023 and the related-work account](../references/RELATED_WORK.md). The argument below controls its local action directly and supplies the response identity needed to recover an entire time-dependent waveform.

## 1. An exact weak-generator representation

Write $`\widehat U(t,s)`$ for the reference propagator. The experimentally implemented pair, with the inverse applied first, is

```math
E_t=U_H(t,0)\widehat U(t,0)^\dagger.
```

Fix an endpoint $`t`$. The following path connects the identity to this right echo:

```math
V_t(s)=
\widehat U(t,0)\widehat U(s,0)^\dagger
U_H(s,0)\widehat U(t,0)^\dagger,
\qquad 0\le s\le t.
```

Indeed, $`V_t(0)=I`$ and $`V_t(t)=E_t`$. Differentiating in $`s`$ gives

```math
\partial_sV_t(s)=-iG_{t,s}V_t(s),
\qquad
G_{t,s}=\widehat U(t,s)R(s)\widehat U(t,s)^\dagger.
```

Thus the echo is exactly the time-ordered evolution of a dressed residual. The dressing can spread each original term, but finite-time locality controls its tails.

Define its integrated first-order response by

```math
L_t=\int_0^tG_{t,s}\,ds.
```

Differentiating with respect to the endpoint gives

```math
L_t'=R(t)-i[\widehat H(t),L_t],
\qquad
R(t)=L_t'+i[\widehat H(t),L_t].
```

The latter equality is the waveform inversion formula. It uses the known reference Hamiltonian and the response at the same time. It requires neither a matrix logarithm of $`E_t`$ nor a lower bound on a separate observability matrix.

## 2. Local interaction moments

The following locality consequence will be used twice.

**Lemma 1.** There are constants $`K_0,K_1`$, depending only on the fixed geometry and reference strength bound, such that every $`G_{t,s}`$ has a Hermitian interaction decomposition $`G_{t,s}=\sum_Zg_Z(t,s)`$ satisfying

```math
J_0(G_{t,s})
:=\sup_i\sum_{Z\ni i}\|g_Z(t,s)\|
\le K_0\delta,
```

```math
J_1(G_{t,s})
:=\sup_i\sum_{Z\ni i}|Z|\,\|g_Z(t,s)\|
\le K_1\delta.
```

Both constants are independent of $`n,m,\delta,s,t`$.

**Proof.** For the support $`X`$ of an original Pauli, let $`X_\ell`$ be its lattice neighborhood of radius $`\ell`$. Let $`\mathbb E_{X_\ell}`$ be the conditional expectation obtained by taking the normalized partial trace over its complement and restoring the exterior identity. This map preserves Hermiticity and is norm contracting.

Finite-time Lieb–Robinson locality for the bounded reference Hamiltonian gives

```math
\left\|
\widehat U(t,s)P_X\widehat U(t,s)^\dagger
-
\mathbb E_{X_\ell}
\bigl(\widehat U(t,s)P_X\widehat U(t,s)^\dagger\bigr)
\right\|
\le c_1e^{-\mu\ell}.
```

A polynomial prefactor in a tail bound can be absorbed into a smaller positive $`\mu`$. This is the same finite-time locality principle underlying the lattice decompositions in [HHKL2020](../references/RELATED_WORK.md). Its constants depend on the maximum instantaneous interaction strength. No time-derivative bound is needed.

Take the conditional expectation at radius zero as the first shell and consecutive differences thereafter. The resulting Hermitian shells are supported in $`X_\ell`$ and have norms at most $`c_2e^{-\mu\ell}`$. They telescope exactly in finite volume. Multiply the shells associated with $`P_a`$ by $`r_a(s)`$ and sum over the original terms.

A ball has at most $`c_3(1+\ell)^D`$ sites. Bounded incidence and bounded original diameter imply that at most $`c_4(1+\ell)^D`$ original-support neighborhoods of radius $`\ell`$ contain any specified site. The two asserted interaction moments are therefore bounded by constant multiples of

```math
\delta\sum_{\ell\ge0}(1+\ell)^D e^{-\mu\ell}
\quad\text{and}\quad
\delta\sum_{\ell\ge0}(1+\ell)^{2D}e^{-\mu\ell}.
```

Both series converge. Duplicate support labels can be retained as separate terms; combining them only decreases the upper bounds. This proves the lemma uniformly in finite volume. $`\square`$

## 3. A local Dyson bound for arbitrarily many repetitions

**Lemma 2.** Let $`Q`$ be a one-site Pauli. For every nonnegative integer $`q`$ and every $`t\in[0,1]`$,

```math
\left\|
E_t^{-q}QE_t^q-Q-iq[L_t,Q]
\right\|
\le 2K_0K_1(qt\delta)^2.
```

**Proof.** Repeat the path $`G_{t,s}`$ for $`q`$ periods. Denote the resulting generator by $`F(s)`$ on $`[0,S]`$, where $`S=qt`$, and its propagator by $`V(s)`$. Then $`V(S)=E_t^q`$ and the two interaction moments retain the bounds in Lemma 1.

If $`Q`$ acts on site $`i`$, an inner term contributing to $`[F(s),Q]`$ must contain $`i`$. Its commutator is supported inside that term's support $`Z`$. An outer contributing term must therefore meet $`Z`$. Consequently,

```math
\begin{aligned}
\|[F(u),[F(s),Q]]\|
&\le
4\sum_{Z\ni i}\|f_Z(s)\|
\sum_{Y:\,Y\cap Z\ne\varnothing}\|f_Y(u)\|\\
&\le4J_1(F(s))J_0(F(u))\\
&\le4K_0K_1\delta^2.
\end{aligned}
```

The exact Heisenberg equation integrates to

```math
V(S)^\dagger QV(S)
=Q+i\int_0^S V(s)^\dagger[F(s),Q]V(s)\,ds.
```

For each fixed outer time $`s`$, integrate the conjugation of the fixed operator $`[F(s),Q]`$ once more. This gives the exact second-order identity

```math
\begin{aligned}
V(S)^\dagger QV(S)
={}&Q+i\int_0^S[F(s),Q]\,ds\\
&-\int_0^S ds\int_0^sdu\,
V(u)^\dagger[F(u),[F(s),Q]]V(u).
\end{aligned}
```

The first integral is $`iq[L_t,Q]`$. Unitary conjugation preserves norm, and the triangular integration region has area $`S^2/2`$. The double-commutator bound proves the claim. $`\square`$

There is no assumption that $`n\delta`$ is small. The estimate itself also does not require $`q\delta`$ to be small; reconstruction chooses a small value to control the resulting bias. A principal Floquet logarithm is never invoked.

## 4. Reading one local coefficient

Let $`P`$ be any nonidentity canonical Hermitian Pauli, and choose a one-site Pauli $`Q`$ that anticommutes with it. Set

```math
B=iPQ,\qquad
l_P(t)=2^{-n}\mathrm{Tr}(PL_t).
```

The operator $`B`$ is a Hermitian signed Pauli, of the same weight as $`P`$, and

```math
[B,Q]=2iP,\qquad \mathrm{Tr}(BQ)=0.
```

Consider the process transfer coefficient

```math
f_{P,t}(q)
=2^{-n}\mathrm{Tr}\bigl(QE_t^qBE_t^{-q}\bigr).
```

Cyclicity and the commutator identity give

```math
i\,2^{-n}\mathrm{Tr}\bigl(B[L_t,Q]\bigr)
=2l_P(t).
```

Taking normalized trace against $`B`$ in Lemma 2 therefore yields

```math
\left|f_{P,t}(q)-2q\,l_P(t)\right|
\le 2K_0K_1(qt\delta)^2.
```

The sign is positive for the stated right echo and for $`B=iPQ`$. Reversing either convention changes the corresponding extraction formula.

There is also a useful coefficient-size estimate. Since

```math
2l_P(t)
=-i\,2^{-n}\mathrm{Tr}\bigl(B[Q,L_t]\bigr),
```

Lemma 1 gives

```math
|l_P(t)|
\le\frac12\|[Q,L_t]\|
\le tK_0\delta
\le K_0\delta.
```

This bound holds for every nonidentity Pauli $`P`$, including the additional local strings required by the waveform inversion.

## 5. Product-state transfer estimator

The required transfer coefficients can be estimated in parallel using product inputs and product measurements. This is a process version of the shadow-estimation framework [H2020; F2026](../references/RELATED_WORK.md); the elementary estimator is proved here to fix its normalization and signs.

Write

```math
B=\sigma_B\bigotimes_jB_j,\qquad
\sigma_B\in\{-1,1\},\qquad
w=|\mathrm{supp}B|.
```

In one snapshot, independently choose a uniform Pauli axis $`a_j\in\{X,Y,Z\}`$ and eigenvalue $`s_j\in\{-1,1\}`$ on each input qubit. Prepare their product eigenstate, apply the repeated echo, and measure every qubit in an independent uniform Pauli axis $`b_j`$. Let $`y_i`$ be the measured eigenvalue at the site of $`Q`$.

Define

```math
X_B=\sigma_B3^w
\prod_{j\in\mathrm{supp}B}
s_j\,\mathbf1\{a_j=B_j\},
\qquad
Y_Q=3y_i\,\mathbf1\{b_i=Q\}.
```

The sign $`\sigma_B`$ is essential: $`iPQ`$ need not have positive canonical Pauli phase.

If $`\rho_{\rm in}`$ is the prepared product state, the single-site identities imply

```math
\mathbb E[X_B\rho_{\rm in}]=\frac{B}{2^n},
\qquad
\mathbb E[Y_Q\mid\rho_{\rm out}]
=\mathrm{Tr}(Q\rho_{\rm out}).
```

Thus $`Z_{B,Q}=X_BY_Q`$ is unbiased for $`f_{P,t}(q)`$. Since signs and measurement outcomes square to one, while the matching events have probabilities $`3^{-w}`$ and $`1/3`$,

```math
\mathbb E[Z_{B,Q}^2]=3^{w+1}.
```

This second-moment bound remains valid for an approximate physical echo channel. The associated implementation bias is treated separately in [reconstruction](reconstruction.md).

The estimator is also bounded by $`|Z_{B,Q}|\le3^{w+1}`$. For $`M_{\rm tar}`$ target pairs of maximum input weight $`w_{\max}`$ and $`0<\eta\le1`$, apply Bernstein's inequality to the sample mean and then a union bound. All transfer coefficients are estimated to error $`\eta`$, with failure probability at most $`\beta`$, from

```math
O\!\left(
3^{w_{\max}+1}\eta^{-2}
\log\frac{M_{\rm tar}}{\beta}
\right)
```

shared snapshots. Correlation between the different target estimators does not affect this union bound.

For the reconstruction below, $`w_{\max}\le2k-1`$ and $`M_{\rm tar}=O(n)`$. Each snapshot still requires preparation and readout of the full register and processing its local records. Those $`O(n)`$ costs are charged in [resources](resources.md).

## 6. The local data required for waveform inversion

For an original ansatz term $`P_a`$, taking its coefficient in the exact response identity gives

```math
r_a(t)
=l_{P_a}'(t)
+i\,2^{-n}\mathrm{Tr}
\bigl([P_a,\widehat H(t)]L_t\bigr).
```

Expand the known commutator as

```math
i[P_a,\widehat H(t)]
=\sum_{S\in\mathcal S_a}c_{a,S}(t)S.
```

Only reference terms meeting $`\mathrm{supp}P_a`$ can contribute. There are at most $`dk`$ of them, every resulting nonidentity Pauli has weight at most $`2k-1`$, and

```math
\sum_{S\in\mathcal S_a}|c_{a,S}(t)|
\le2dk\bar J.
```

The union of all required strings therefore contains $`O(n)`$ constant-weight Paulis, determined by the known interaction pattern. This completes the reduction from waveform learning to local transfer data. [The next page](reconstruction.md) bounds the derivative step and assembles an explicit contraction.
