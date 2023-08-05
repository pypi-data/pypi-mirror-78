# -*- coding: utf-8 -*-

import pytest
from qpz_atomics.skeleton import fib

__author__ = "Harold Ollivier"
__copyright__ = "Harold Ollivier"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
