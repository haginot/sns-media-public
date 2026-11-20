from functools import lru_cache
def count(n):
    @lru_cache(None)
    def f(i,mask):
        if i==n: return 1
        return sum(f(i+1,mask|1<<j) for j in range(n) if not mask>>j&1 and abs(j-i)!=1)
    return f(0,0)
for n in range(1,13): print(n,count(n))
def count2(n,bad):
    @lru_cache(None)
    def f(i,mask):
        if i==n: return 1
        return sum(f(i+1,mask|1<<j) for j in range(n) if not mask>>j&1 and abs(j-i) not in bad)
    return f(0,0)
print("n=8 no |d| in {1,2}:",count2(8,(1,2)))
