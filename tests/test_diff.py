"""Tests for text diff."""

import pytest
from text_diff import diff, lcs_length
from text_diff.diff import Op, format_diff


class TestDiff:
    def test_lcs_length(self):
        assert lcs_length("ABCBDAB", "BDCAB") == 4
        assert lcs_length("", "") == 0
        assert lcs_length("abc", "abc") == 3

    def test_identical(self):
        lines = diff("abc", "abc")
        assert all(d.op == Op.KEEP for d in lines)

    def test_insertion(self):
        lines = diff("ac", "abc")
        assert any(d.op == Op.INSERT and d.value == "b" for d in lines)

    def test_deletion(self):
        lines = diff("abc", "ac")
        assert any(d.op == Op.DELETE and d.value == "b" for d in lines)

    def test_format(self):
        lines = diff(["a", "b"], ["a", "c", "b"])
        formatted = format_diff(lines)
        assert "+c" in formatted
