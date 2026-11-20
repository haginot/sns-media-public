### Problem 1

We want the number of permutations $p$ of $\{1, \dots, 10\}$ avoiding the forbidden board $B_{10} = \{(i,j) : |i - j| = 1\}$.

View $B_{10}$ as a bipartite graph between rows $\{1,\dots,10\}$ and columns $\{1,\dots,10\}$. Every forbidden cell $(i,j)$ has $i$ and $j$ of opposite parity, so $B_{10}$ splits into two vertex-disjoint components:
1. Odd rows and even columns: the path $r_1 - c_2 - r_3 - c_4 - \dots - r_9 - c_{10}$ (9 edges).
2. Even rows and odd columns: the path $c_1 - r_2 - c_3 - r_4 - \dots - c_9 - r_{10}$ (9 edges).

A placement of $k$ non-attacking rooks on a path of $m=9$ edges corresponds to choosing $k$ non-adjacent edges, which can be done in $\binom{10-k}{k}$ ways. Thus each component has rook polynomial
$$f_9(x) = \sum_{k=0}^{5} \binom{10-k}{k} x^k = 1 + 9x + 28x^2 + 35x^3 + 15x^4 + x^5.$$
Since the two components share no rows or columns, the rook polynomial of $B_{10}$ is
$$R(x) = (f_9(x))^2 = 1 + 18x + 137x^2 + 574x^3 + 1444x^4 + 2232x^5 + 2083x^6 + 1106x^7 + 295x^8 + 30x^9 + x^{10}.$$

By inclusion–exclusion, the number of valid permutations is $\sum_{k=0}^{10} (-1)^k r_k (10-k)!$:
- Even $k$ (positive): $1(3628800) + 137(40320) + 1444(720) + 2083(24) + 295(2) + 1(1) = 3628800 + 5523840 + 1039680 + 49992 + 590 + 1 = 10242903$.
- Odd $k$ (negative): $18(362880) + 574(5040) + 2232(120) + 1106(6) + 30(1) = 6531840 + 2892960 + 267840 + 6636 + 30 = 9699306$.

Subtracting gives $10242903 - 9699306 = 543597$.

---

### Problem 2

We want the permanent of the $8 \times 8$ allowed matrix $A$ where $A_{i,j} = 1$ iff $|i-j| = 0$ or $|i-j| \ge 3$.

Partition $\{1,\dots,8\}$ into $U = \{1,2,3\}$, $M = \{4,5\}$, and $L = \{6,7,8\}$.
- Inside $U \times U$ and $L \times L$, only diagonal entries $(i,i)$ are allowed.
- Every entry in $U \times L$ and $L \times U$ is allowed (since $|i-j| \ge 3$).
- In $M$: row/col 4 allows $\{1,4,7,8\}$, and row/col 5 allows $\{1,2,5,8\}$.

Once rows $4,5$ and columns $4,5$ are assigned, suppose the remaining rows and columns in $U$ and $L$ have sizes $(r_1, c_1)$ and $(r_2, c_2)$, with $a = |R_U \cap C_U|$ and $b = |R_L \cap C_L|$ available fixed points. Choosing $k_1$ fixed points in $U$ forces $k_2 = k_1 + r_2 - c_1$ fixed points in $L$, and the remaining rows of $U$ (resp. $L$) map arbitrarily to the remaining columns of $L$ (resp. $U$), giving
$$F(r_1, c_1, a;\; r_2, c_2, b) = \sum_{k_1} \binom{a}{k_1}\binom{b}{k_1 + r_2 - c_1}(r_1-k_1)!(c_1-k_1)!.$$

We split into four cases based on whether $p(4)=4$ and $p(5)=5$:
1. **$p(4)=4, p(5)=5$:** $F(3,3,3;\; 3,3,3) = \sum_{k=0}^3 \binom{3}{k}^2 ((3-k)!)^2 = 36+36+9+1 = 82$.
2. **$p(4)=4, p(5)\neq 5$:** Choose $i = p^{-1}(5) \in \{1,2,8\}$ and $j = p(5) \in \{1,2,8\}$ (9 pairs):
   - $i=j \in \{1,2\}$ (2 pairs): $F(2,2,2;\; 3,3,3) = 19 \implies 38$.
   - $i\neq j \in \{1,2\}$ (2 pairs): $F(2,2,1;\; 3,3,3) = 15 \implies 30$.
   - $i \in \{1,2\}, j=8$ (2 pairs): $F(2,3,2;\; 3,2,2) = 21 \implies 42$.
   - $i=8, j \in \{1,2\}$ (2 pairs): $F(3,2,2;\; 2,3,2) = 21 \implies 42$.
   - $i=j=8$ (1 pair): $F(3,3,3;\; 2,2,2) = 19 \implies 19$.
   Total for Case 2: $38+30+42+42+19 = 171$.
3. **$p(4)\neq 4, p(5)=5$:** By the symmetry $i \mapsto 9-i$, also $171$.
4. **$p(4)\neq 4, p(5)\neq 5$:** The ordered pair $(i_4, i_5) = (p^{-1}(4), p^{-1}(5))$ can be any of 7 valid pairs, yielding the multiset of removed row pairs $I$: $\{1,2\}$ (mult 1, type $A$), $\{7,8\}$ (mult 1, type $B$), and type $C$: $\{1,8\}$ (mult 2), $\{1,7\}$ (mult 1), $\{2,7\}$ (mult 1), $\{2,8\}$ (mult 1). The removed column pairs $J = \{p(4), p(5)\}$ have the exact same multiset. Summing over all type pairs $(I, J)$:
   - $(A,A)$ and $(B,B)$: each $1 \times F(1,1,1;\; 3,3,3) = 4 \implies 8$.
   - $(A,B)$ and $(B,A)$: each $1 \times F(1,3,1;\; 3,1,1) = 8 \implies 16$.
   - $(A,C), (C,A), (B,C), (C,B)$: each $5 \times F(1,2,1;\; 3,2,2) = 5 \times 5 = 25 \implies 100$.
   - $(C,C)$: $r_1=c_1=r_2=c_2=2$, and $F(2,2,a;\;2,2,b)$ equals $9, 6, 6, 5$ for $(a,b) = (2,2), (2,1), (1,2), (1,1)$, with total weights $7, 6, 6, 6$ respectively: $7(9) + 6(6) + 6(6) + 6(5) = 165$.
   Total for Case 4: $8 + 16 + 100 + 165 = 289$.

Summing all four cases gives $82 + 171 + 171 + 289 = 713$.

---

### Problem 3

1. By (a) and (i), Aoi, Python, and Java occupy three consecutive slots $x, x+1, x+2$ ($x \in \{1,2,3\}$).
2. Test each value of $x$ using (h) ($\text{Swift} \in \{2,4\}$), (g) (Rust and Swift not adjacent), and (c) ($\text{Go} < \text{Swift}, \text{Java}$):
   - If $x=1$ (1: Aoi, 2: Python, 3: Java): Swift must be 4. Since Rust cannot be adjacent to 4, Rust is 1 and Go is 5, violating $\text{Go} < \text{Swift}$.
   - If $x=3$ (3: Aoi, 4: Python, 5: Java): Swift must be 2. Then Rust must be 1 or 3, both adjacent to 2, violating (g).
   - Thus $x=2$: 2 is Aoi, 3 is Python, 4 is Java. By (h), Swift must be 2 (so Aoi uses Swift). By (c), Go must be earlier than Swift (2), so Go is 1, leaving Rust at 5. (This satisfies (g) since $|5-2|=3 \ge 2$.)
3. Assign the remaining people to slots 1, 3, 4, 5:
   - By (b), Ben is in $\{2,3,4\}$ and does not use Python (3). Since Aoi is in 2, Ben is in slot 4 (Java).
   - By (d), Chika is later than Ben (4), so Chika is in slot 5 (Rust).
   - By (e), Emi is two slots away from Chika (5), so Emi is in slot 3 (Python).
   - The remaining person, Daiki, is in slot 1 (Go), which is odd, satisfying (f).

ANSWER 1: 543597
ANSWER 2: 713
ANSWER 3: 1: Daiki, Go; 2: Aoi, Swift; 3: Emi, Python; 4: Ben, Java; 5: Chika, Rust