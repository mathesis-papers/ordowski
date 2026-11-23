# Ordowski's prime-offset conjecture

This package contains a self-contained Fermat-number proof of the conjecture in the first COMMENTS line of [OEIS A369378](https://oeis.org/A369378), revision 40 (13 February 2024), and an exact greatest-common-divisor formula for the associated sums and absolute differences.

## Contents

- `note.tex`: complete LaTeX source, with the bibliography included.
- `note.pdf`: readable mathematical note.
- `verify.py`: dependency-free exact-integer finite checker, requiring Python 3.8 or later.
- `verification.json`: expected output of the checker.
- `metadata.json`: title, authors, license, and statement identity.

## Build and check

Build with **Tectonic 0.17.0**:

```sh
tectonic note.tex
```

Alternatively, use a standard LaTeX distribution:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

The bibliography is embedded in `note.tex`; no BibTeX step or separate `.bib` file is needed.

Run the finite calculations and compare their exact output:

```sh
python3 verify.py > actual.json
cmp actual.json verification.json
```

The checker tests both gcd identities for `1 <= n <= 12` and `0 <= k,m < 4*2^n`, the original conjecture for every `0 <= k < 2^n` in that range, proper-divisor conditions, four least prime offsets, Wu's linked conjecture for `3 <= j <= 12`, and finite instances of the two all-prime-family obstructions for every `1 <= C <= 99`. It uses no floating-point arithmetic or probabilistic primality tests.

## Mathematical coverage

For `n >= 1`, every positive exponent `k` not divisible by `2^n` gives a composite value of `2^(2^n+1)-1+2^k`; the exponent zero does too. Hence every existing least prime offset is a positive multiple of `2^n`. This is a necessary condition, not an existence assertion or a sufficient primality test.

The pinned [Lean file](https://github.com/the-omega-institute/trureturing/blob/a89e0fb9ba0f9002502ec8125455c2c2a9281443/D5/S3/Arith/Primes/OeisA369378FermatCovering.lean), declaration `D5.S3.Arith.Primes.OeisA369378FermatCovering.result`, formalizes the original range `n > 0`, `k < 2^n`, including `k=0`. The gcd identities, unrestricted-exponent consequence, absolute-difference consequence, and all-prime-family proposition have written proofs in the note. The calculations in `verification.json` cover exactly the listed finite ranges.

The full absolute-difference conjecture for `n > 5` is not established: the class `m = -1 (mod 2^n)` remains outside the Fermat-divisor obstruction, apart from the explicit nonprime value 1 at `m=2^n-1`. No Sierpiński or Riesel classification of these numbers is asserted.

For the source's least reverse prime offset `b(n)`, existence with `n >= 3` implies `b(n) = -1 (mod 2^n)` and `b(n) >= 2^(n+1)-1`.

The note also reproves Chai Wah Wu's A138290 conjecture, credited to Crocker's 1971 lemma and Ordowski's March 2024 proof pointer, and deduces `A208083(2^j-1)=0` for `j>=3`. Its A076336 S3/S4 result credits Don Reble's 2022 proofs as recorded in Richard J. Mathar's January 2024 note; explicit progressions give infinitely many composite terms for every positive base. Source locators and the remaining questions appear in the note's coverage table.

## Authors and license

1. Haobo Ma — ChronoAI Pte Ltd, Singapore.
2. Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore.

Copyright 2026 Haobo Ma and Wenlin Zhang. Licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)**, identifier `cc-by-4.0`.
