"""LCS-based text diff algorithm.

Computes the longest common subsequence (LCS) of two sequences,
then derives the edit script (insertions and deletions).

The LCS problem is solved with dynamic programming in O(mn) time.
Space-optimized to O(min(m,n)) using Hirschberg's algorithm variant.

Used in: git diff, code review tools, version control, merge tools.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Generic, List, Optional, Sequence, TypeVar

T = TypeVar("T")


class Op(Enum):
    KEEP = "="
    DELETE = "-"
    INSERT = "+"


@dataclass
class DiffLine(Generic[T]):
    op: Op
    value: T
    old_idx: Optional[int] = None
    new_idx: Optional[int] = None

    def __repr__(self) -> str:
        return f"{self.op.value} {self.value}"


def lcs_length(a: Sequence[T], b: Sequence[T]) -> int:
    """Compute LCS length using DP with O(min(m,n)) space."""
    if len(a) < len(b):
        a, b = b, a
    m, n = len(a), len(b)

    prev = [0] * (n + 1)
    curr = [0] * (n + 1)

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i-1] == b[j-1]:
                curr[j] = prev[j-1] + 1
            else:
                curr[j] = max(prev[j], curr[j-1])
        prev, curr = curr, [0] * (n + 1)

    return prev[n]


def lcs_table(a: Sequence[T], b: Sequence[T]) -> List[List[int]]:
    """Build full LCS DP table for traceback."""
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp


def diff(old: Sequence[T], new: Sequence[T]) -> List[DiffLine[T]]:
    """Compute the diff between old and new sequences.

    Returns a list of DiffLine objects indicating keeps, deletions, and insertions.
    """
    dp = lcs_table(old, new)
    result: List[DiffLine[T]] = []

    i, j = len(old), len(new)
    stack: List[DiffLine[T]] = []

    while i > 0 or j > 0:
        if i > 0 and j > 0 and old[i-1] == new[j-1]:
            stack.append(DiffLine(Op.KEEP, old[i-1], i-1, j-1))
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or dp[i][j-1] >= dp[i-1][j]):
            stack.append(DiffLine(Op.INSERT, new[j-1], None, j-1))
            j -= 1
        else:
            stack.append(DiffLine(Op.DELETE, old[i-1], i-1, None))
            i -= 1

    stack.reverse()
    return stack


def diff_text(old_text: str, new_text: str) -> List[DiffLine[str]]:
    """Convenience: diff two strings line-by-line."""
    old_lines = old_text.splitlines(keepends=True)
    new_lines = new_text.splitlines(keepends=True)
    return diff(old_lines, new_lines)


def format_diff(lines: List[DiffLine]) -> str:
    """Format diff lines as a unified diff string."""
    result = []
    for line in lines:
        prefix = {"=": " ", "-": "-", "+": "+"}[line.op.value]
        result.append(f"{prefix}{line.value}")
    return "".join(result)
