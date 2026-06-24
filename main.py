#!/usr/bin/env python3
"""Text Diff demo."""

from text_diff import diff, lcs_length
from text_diff.diff import format_diff


def main():
    print("=== Text Diff (LCS) Demo ===
")

    old = "the quick brown fox
jumps over the lazy dog
"
    new = "the quick red fox
jumps over the lazy dog
and the cat
"

    print(f"LCS length: {lcs_length(old, new)}")
    print()

    lines = diff(old.splitlines(), new.splitlines())
    for line in lines:
        print(f"  {line}")


if __name__ == "__main__":
    main()
