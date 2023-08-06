from hypothesis import strategies as st, given, assume


class TestUO:

    @given(st.integers())
    def test_non_brand(self, i):
        assume(i)
        assert i is not None
