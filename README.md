# Text Diff (LCS)

A longest-common-subsequence (LCS) based diff algorithm — the same algorithm behind `git diff` and most version control systems.

## How It Works

1. **LCS Table:** Build an (m+1) × (n+1) DP table where `dp[i][j]` = length of the LCS of `old[:i]` and `new[:j]`.

2. **Traceback:** Walk the table from `(m, n)` to `(0, 0)`. At each cell:
   - If `old[i-1] == new[j-1]`: diagonal move → KEEP.
   - If `dp[i-1][j] >= dp[i][j-1]`: up move → DELETE old[i-1].
   - Otherwise: left move → INSERT new[j-1].

3. The traceback produces an edit script: a sequence of keeps, deletions, and insertions that transforms old into new.

The LCS itself is the subsequence of KEEP operations.

## Complexity

| Operation | Time | Space |
|-----------|------|-------|
| LCS length | O(m·n) | O(min(m,n)) — space-optimized |
| Full diff  | O(m·n) | O(m·n) — for traceback |

Where m = len(old), n = len(new).

## Applications

**Version Control:** git diff, svn diff — show what changed between commits. Myers' diff algorithm (used in practice) is a refinement of LCS-based diff.

**Code Review:** GitHub PRs, Gerrit, Phabricator — all display diffs computed from LCS.

**Merge Tools:** Three-way merge (base, ours, theirs) uses LCS to identify conflicting changes.

**Document Comparison:** Word's "Track Changes," Google Docs version history — line or word level diffing.

**Bioinformatics:** Sequence alignment (Needleman-Wunsch, Smith-Waterman) are LCS variants with scoring matrices and gap penalties.
