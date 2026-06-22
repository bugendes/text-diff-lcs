#!/usr/bin/env python3
"""Text diff using Longest Common Subsequence."""

def lcs(a, b):
    m, n = len(a), len(b)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            dp[i][j] = dp[i-1][j-1]+1 if a[i-1]==b[j-1] else max(dp[i-1][j], dp[i][j-1])
    result = []; i, j = m, n
    while i > 0 and j > 0:
        if a[i-1] == b[j-1]: result.append(a[i-1]); i -= 1; j -= 1
        elif dp[i-1][j] > dp[i][j-1]: i -= 1
        else: j -= 1
    return result[::-1]

def diff(old, new):
    l = lcs(old, new)
    result = []; oi = ni = li = 0
    while oi < len(old) or ni < len(new):
        if li < len(l):
            while oi < len(old) and old[oi] != l[li]: result.append(f"- {old[oi]}"); oi += 1
            while ni < len(new) and new[ni] != l[li]: result.append(f"+ {new[ni]}"); ni += 1
            result.append(f"  {l[li]}"); oi += 1; ni += 1; li += 1
        else:
            while oi < len(old): result.append(f"- {old[oi]}"); oi += 1
            while ni < len(new): result.append(f"+ {new[ni]}"); ni += 1
    return result

if __name__ == "__main__":
    old = "def hello():\n    print('hello')\n    return True".split("\n")
    new = "def hello(name='world'):\n    print(f'hello {name}')\n    return True".split("\n")
    for line in diff(old, new): print(f"  {line}")\n