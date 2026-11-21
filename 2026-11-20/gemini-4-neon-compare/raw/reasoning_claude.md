**Problem 1**

Use inclusion–exclusion with rook polynomials. The forbidden cells are the two off-diagonals, (i, i+1) and (i+1, i).

- These 18 cells split into two independent "zig-zag" paths of 9 cells each. In each path, consecutive cells attack each other.
- On a path of 9 cells, the number of ways to place a non-attacking rooks is C(10−a, a). This gives the polynomial f(x) = 1 + 9x + 28x² + 35x³ + 15x⁴ + x⁵.
- The rook polynomial of the whole board is f(x)²:
  r = 1, 18, 137, 574, 1444, 2232, 2083, 1106, 295, 30, 1.
- The count is Σ(−1)ᵏ rₖ (10−k)!:
  3628800 − 6531840 + 5523840 − 2892960 + 1039680 − 267840 + 49992 − 6636 + 590 − 30 + 1 = **543597**.
- Sanity check: the same formula gives 5 for n = 4, which matches direct enumeration.

**Problem 2**

The forbidden cells are those with offset ±1 or ±2.

- Compute the rook polynomial with a row-by-row transfer. The state is which of the columns i−1, i, i+1, i+2 are already used.
- The coefficients obtained are r = 1, 26, 261, 1294, 3372, 4550, 2933, 746, 45.
- Checks:
  - r₁ = 26 is the number of forbidden cells.
  - r₂ = 261 matches a direct pair count.
  - r₈ = 45 matches a separate count of permutations whose displacements are all in {±1, ±2}.
  - Every intermediate stage checks out when evaluated at x = ±1.
- The count is Σ(−1)ᵏ rₖ (8−k)!:
  40320 − 131040 + 187920 − 155280 + 80928 − 27300 + 5866 − 746 + 45 = **713**.

**Problem 3**

- From (a) and (i), Aoi, the Python presenter and the Java presenter are in three consecutive slots k, k+1, k+2.
- **k = 1:** Go must come before Java and cannot be in slot 2, so Go is in slot 1. Swift is even, so slot 4, and Rust is in slot 5. Rust and Swift are adjacent, which violates (g). ✗
- **k = 3:** Swift is even, so slot 2. Go comes before Swift, so slot 1, and Rust is in slot 3. Rust and Swift are adjacent. ✗
- **k = 2:** Aoi is in slot 2, Python in 3, Java in 4. Swift is even, so slot 2. Go comes before Swift, so slot 1, and Rust is in slot 5 (not adjacent to Swift ✓).
  - Ben is in slot 2, 3 or 4 and does not use Python, so Ben is in slot 4 (Java).
  - Chika is later than Ben, so slot 5. Emi is two slots from Chika, so slot 3.
  - Daiki takes slot 1, which is odd ✓.

ANSWER 1: 543597
ANSWER 2: 713
ANSWER 3: 1: Daiki, Go; 2: Aoi, Swift; 3: Emi, Python; 4: Ben, Java; 5: Chika, Rust