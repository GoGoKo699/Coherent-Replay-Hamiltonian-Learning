# Reconstruction and contraction

The response identity in [local response](local_response.md) turns each local waveform into a derivative of a measurable transfer coefficient plus a known commutator correction. This page gives the conditioning bounds and an explicit refinement algorithm. The constants are deliberately conservative; the result concerns polynomial degree dependence and the inverse-precision exponent.

All times are normalized to $`[0,1]`$. The coefficient functions $`h_a`$ and the finite-difference spacing $`h`$ are different quantities. The [model](model.md) specifies the access assumptions and physical-unit conversion; [resources](resources.md) accounts for initialization, controls, processing and output.

## 1. Derivative conditioning from the polynomial promise

Let the current degree-$`m`$ reference have coefficient norm at most $`\bar J=2(J+1)`$, and suppose

```math
\max_a\|h_a-\widehat h_a\|_\infty\le\delta.
```

For any nonidentity Pauli $`S`$ of weight $`w`$, the local response proof gives $`|l_S|\le K_0\delta`$. Taking the coefficient of $`S`$ in the response differential equation then gives

```math
|l_S'(t)|
\le\bigl(1+2dw\bar J K_0\bigr)\delta.
```

The leading residual coefficient is zero when $`S`$ is absent from the original ansatz. There are at most $`dw`$ overlapping reference terms, which explains the second term.

For an original Hamiltonian string $`P_a`$, differentiate once more:

```math
\begin{aligned}
l_{P_a}''(t)
={}&r_a'(t)
-i\,2^{-n}\mathrm{Tr}
\bigl([P_a,\widehat H'(t)]L_t\bigr)\\
&-i\,2^{-n}\mathrm{Tr}
\bigl([P_a,\widehat H(t)]L_t'\bigr).
\end{aligned}
```

Markov's inequality on $`[0,1]`$ bounds the derivative of a degree-$`m`$ polynomial by $`2m^2`$ times its uniform norm; see [Trefethen2013](../references/RELATED_WORK.md). Hence

```math
\|r_a'\|_\infty\le2m^2\delta,
\qquad
\|\widehat h_a'\|_\infty\le2m^2\bar J.
```

With $`M_0=2dk\bar J`$, the preceding local coefficient bounds give the explicit estimate

```math
\begin{aligned}
|l_{P_a}''(t)|\le\delta\bigl[
&2m^2+4dk\bar J K_0m^2\\
&+M_0\bigl(1+2d(2k-1)\bar J K_0\bigr)
\bigr].
\end{aligned}
```

In particular, $`|l_{P_a}''|\le C(1+m^2)\delta`$ for a known constant independent of $`n,m,\delta`$. The derivative is conditioned by the local residual size, even if the global operator-norm residual is extensive.

Choose one constant $`C\ge1`$, depending only on the fixed geometry and $`J`$, large enough that every bounded reference obeys all of

```math
|l_S(t)|\le C\delta,\qquad
|l_{P_a}''(t)|\le C(1+m^2)\delta,
```

```math
\sum_{S\in\mathcal S_a}|c_{a,S}(t)|\le C,\qquad
|f_{P,t}(q)-2ql_P(t)|\le C(q\delta)^2.
```

The explicit estimates here and in [Lemmas 1–2](local_response.md) supply such a constant. These bounds require no numerical assessment of an unknown conditioning matrix.

## 2. Fixed times and explicit accuracy scales

Set

```math
\Lambda=2+\log(m+1),\qquad
h=\frac{1}{128C(1+m^2)\Lambda},
```

```math
\tau=\frac{h}{128C\Lambda},\qquad
\eta=\frac{\tau h}{128\Lambda},\qquad
\delta_0=\frac{\tau}{2}.
```

For $`m\ge1`$, use the $`m+1`$ shifted Chebyshev–Lobatto nodes

```math
t_i=\frac{1-\cos(i\pi/m)}2,\qquad i=0,\ldots,m.
```

Their interpolation operator has uniform norm at most the conservative bound $`\Lambda`$ [Trefethen2013](../references/RELATED_WORK.md). For $`m=0`$, use the single node $`t_0=1/2`$; the true interpolation norm is one, and retaining $`\Lambda=2`$ only enlarges the safety margin.

At each node, define a one-sided difference

```math
D_h l(t_i)=
\begin{cases}
\bigl(l(t_i+h)-l(t_i)\bigr)/h,&t_i\le1-h,\\[2mm]
\bigl(l(t_i)-l(t_i-h)\bigr)/h,&t_i>1-h.
\end{cases}
```

Every query time is in $`[0,1]`$. At most $`2(m+1)`$ distinct times are needed. They depend on the degree and fixed physical bounds, but are unchanged through precision refinement. The mean-value integral remainder gives

```math
|D_hl_{P_a}(t_i)-l_{P_a}'(t_i)|
\le\frac h2\|l_{P_a}''\|_\infty
\le\frac{\delta}{256\Lambda}.
```

The polynomial promise applies to the residual coefficients $`r_a`$. The response functions $`l_P`$ themselves need not be polynomials; the finite-difference bound above is sufficient.

## 3. One refinement step

Suppose that the current declared radius satisfies $`0<\delta\le\delta_0`$. Use

```math
q=\left\lfloor\frac{\tau}{\delta}\right\rfloor.
```

Since $`\tau/\delta\ge2`$,

```math
\frac{\tau}{2\delta}\le q\le\frac{\tau}{\delta}.
```

At each required time, apply $`q`$ right echoes. Require the implemented channel of each complete echo pair to differ from its ideal channel by diamond norm at most

```math
\mu=\frac{\delta h}{128\Lambda}.
```

When the unknown prefix is ideal, this can all be allocated to the known inverse: its unitary operator-norm error $`\nu`$ gives channel error at most $`2\nu`$. With imperfect replay, the complete-pair budget is shared between the inverse and the unknown prefix. The complete implementation cost and sufficient allocations are given in [resources](resources.md#implementation-accuracy-and-noise).

Estimate every needed transfer coefficient to additive statistical accuracy $`\eta`$ using the product process estimator. Write its estimate as $`\widehat f_{P,t}`$ and define

```math
\widetilde l_P(t)=\frac{\widehat f_{P,t}}{2q}.
```

There are three separate contributions to its error. Statistical estimation gives

```math
\frac{\eta}{2q}\le\frac{\delta h}{128\Lambda}.
```

The local echo nonlinearity gives

```math
\frac{C(q\delta)^2}{2q}
\le\frac{C\tau\delta}{2}
=\frac{\delta h}{256\Lambda}.
```

Finally, a channel hybrid bound over the $`q`$ approximate echo pairs gives total channel error at most $`q\mu`$. Since $`\|B/2^n\|_1=1`$ and $`\|Q\|=1`$, the corresponding transfer error is at most $`q\mu`$. The input $`B/2^n`$ is signed, but the diamond norm bounds its induced trace-norm error as well: decompose it into positive and negative parts, whose traces sum to one, and apply the channel bound to each. There is no extra factor of the Hilbert-space dimension. After division by $`2q`$, it contributes

```math
\frac{\mu}{2}\le\frac{\delta h}{256\Lambda}.
```

On the simultaneous statistical success event, every required response value therefore satisfies

```math
|\widetilde l_P(t)-l_P(t)|
\le e_l:=\frac{\delta h}{64\Lambda}.
```

At node $`t_i`$, recover a residual coefficient by

```math
\widetilde r_a(t_i)=
D_h\widetilde l_{P_a}(t_i)
+\sum_{S\in\mathcal S_a}c_{a,S}(t_i)\widetilde l_S(t_i).
```

The reference coefficients in $`c_{a,S}`$ are the known coefficients of the stored current model. Their error relative to the true Hamiltonian has already been incorporated into the residual $`R`$; it is not an additional unknown correction here.

The two differenced value errors contribute at most $`2e_l/h`$, and the commutator contributes at most $`Ce_l`$. Combining these with the finite-difference bias, and using $`Ch\le1`$, gives

```math
\begin{aligned}
|\widetilde r_a(t_i)-r_a(t_i)|
&\le\frac{\delta}{256\Lambda}
+\left(\frac2h+C\right)\frac{\delta h}{64\Lambda}\\
&\le\frac{13\delta}{256\Lambda}.
\end{aligned}
```

Interpolate the $`m+1`$ node values with a polynomial $`\widetilde r_a`$ of degree at most $`m`$. Because the true $`r_a`$ already has that degree,

```math
\|\widetilde r_a-r_a\|_\infty
\le\frac{13\delta}{256}
<\frac{\delta}{8}.
```

Update the model by adding $`\widetilde r_a`$ to $`\widehat h_a`$. Allocate uniform error at most $`\delta/8`$ to all numerical arithmetic and representation of this update. For example, use at most $`\delta/16`$ for certified polynomial arithmetic and round each final shifted Chebyshev coefficient within $`\delta/[16(m+1)]`$. Every basis polynomial has uniform norm one, so these allocations suffice. Then

```math
\|h_a-\widehat h_a^{\,\mathrm{new}}\|_\infty
\le\frac{45\delta}{256}
<\frac{\delta}{4}
<\frac{\delta}{2}.
```

Thus a declared-radius contraction by one half is valid, with slack for certified arithmetic. Every iterate remains a degree-$`m`$ polynomial on the same interaction pattern.

## 4. Bounded controllers on every history

The successful iterates have bounded amplitudes automatically. A resource statement also needs to control what happens when a statistical estimate fails.

Use a uniform grid on $`[0,1]`$, including its endpoints, with spacing at most

```math
\Delta_{\rm guard}\le\frac{1}{8(1+m^2)}.
```

After initialization and every update, abort if any polynomial coefficient has magnitude greater than $`J+1/2`$ at any guard point.

To prove that an accepted model is bounded everywhere, let $`p`$ be one of its degree-$`m`$ coefficient polynomials and put $`M_p=\|p\|_\infty`$. A nearest grid point is within $`\Delta_{\rm guard}/2`$ of a maximizer. Markov's inequality gives

```math
M_p
\le\max_{\rm grid}|p|
+m^2\Delta_{\rm guard}M_p.
```

Therefore acceptance implies

```math
M_p\le\frac87\left(J+\frac12\right)<2(J+1)=\bar J.
```

For a concrete finite-precision guard, evaluate each grid value with absolute error at most $`1/16`$ and accept only when every computed magnitude is at most $`J+3/8`$. Acceptance then guarantees true grid magnitudes at most $`J+7/16<J+1/2`$, so the preceding bound still applies. On the good event, every iterate has norm at most $`J+\delta_0`$, with $`\delta_0<1/4`$. Its computed magnitudes are therefore below $`J+5/16<J+3/8`$, and the guard never aborts.

The guard preserves the polynomial class. Pointwise clipping would generally destroy that class and should not replace this check. A bad but accepted estimate can affect accuracy, but cannot create unbounded controls or an unbounded execution cost.

## 5. Paid initialization

The algorithm does not assume that a sufficiently accurate model is supplied. Initialize to error $`\delta_0`$ using the exact-polynomial closed-system specialization of the full-waveform learner [F2026, arXiv:2510.08500v2](../references/RELATED_WORK.md), with failure probability at most $`\rho/2`$. Retain its raw degree-$`m`$ polynomial interpolants and apply the guard above. The authoritative [paid-initialization argument](resources.md#paid-initialization) proves the polynomial degree dependence, distinguishes the analytic localization region from the constant-size probe SDPs, and accounts for samples and classical processing.

## 6. Iteration and adaptive confidence

Set

```math
\delta_s=\delta_0\,2^{-s}.
```

If $`\epsilon\ge\delta_0`$, the successful initializer already meets the target. Otherwise let

```math
K=\left\lceil\log_2\frac{\delta_0}{\epsilon}\right\rceil
```

and perform the refinement step at stages $`s=0,\ldots,K-1`$. At stage $`s`$, use the predetermined radius $`\delta_s`$, set $`q_s=\lfloor\tau/\delta_s\rfloor`$, and allocate total statistical failure probability $`\rho/(2K)`$ across all required time settings and local coefficients.

Each stage uses fresh snapshots. Conditional on any past history, the selected circuit is fixed, and the product estimator has the same universal second-moment bound. The usual concentration guarantee therefore holds conditionally even though the reference model is adaptive. There is no union bound over all possible reference Hamiltonians.

The union of the initializer failure and all stage failures has probability at most $`\rho`$. On its complement, induction applies the contraction at every stage, the guard always passes, and the final error is at most $`\delta_K\le\epsilon`$.

## 7. Refinement resource count

The target Pauli set contains $`O(n)`$ strings of weight at most $`2k-1`$, and there are at most $`2(m+1)`$ time settings. At each setting in one stage, a sufficient shared snapshot count is

```math
N_{\rm shot}
=O\!\left(
3^{2k}\eta^{-2}
\log\frac{C_0n(m+1)\max\{K,1\}}{\rho}
\right),
```

where $`C_0`$ depends on the fixed interaction pattern bounds.

This count is independent of the current precision radius. The precision gain comes from the increasing coherent repetition count in each shot. For nonempty refinement,

```math
\sum_{s=0}^{K-1}q_s
<\frac{2\tau}{\epsilon}.
```

The number of unknown prefix calls, and an upper bound on normalized unknown-evolution time, are consequently

```math
O\!\left(
\frac{(m+1)\Lambda^3h^{-3}}{\epsilon}
\log\frac{C_0n(m+1)\max\{K,1\}}{\rho}
\right).
```

Fixed local factors, including $`3^{2k}`$ and powers of $`C`$, are suppressed here. Substituting $`h`$ yields

```math
O\!\left(
\frac{(m+1)(1+m^2)^3\Lambda^6}{\epsilon}
\log\frac{C_0n(m+1)\max\{K,1\}}{\rho}
\right).
```

Fresh product preparations scale instead as

```math
O\!\left(
(m+1)(1+m^2)^4\Lambda^8K
\log\frac{C_0n(m+1)\max\{K,1\}}{\rho}
\right).
```

The maximum coherent repetition count is $`O(\tau/\epsilon)`$. A fixed implementation defect per echo would eventually overwhelm the contraction, because the required $`\mu`$ decreases with $`\delta_s`$.

These bounds complete the reconstruction proof. [The resource ledger](resources.md) adds paid initialization, inverse compilation, full-register preparation and readout, numerical precision, classical processing and output. The inherited amplification mechanism and the stronger access used here are distinguished from earlier methods in [related work](../references/RELATED_WORK.md).
