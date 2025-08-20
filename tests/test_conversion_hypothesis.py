from hypothesis import given, strategies as st
import math

from src.main import parse_facts, answer_query

FACTS = [
    ("m", 3.28, "ft"),
    ("ft", 12, "in"),
    ("hr", 60, "min"),
    ("min", 60, "sec")
]
graph = parse_facts(facts=FACTS)

length_units = ["m", "ft", "in"]
time_units = ["hr", "min", "sec"]

@given(
    amount = st.floats(min_value=0.01, max_value=100.0),
    unit1 = st.sampled_from(length_units),
    unit2 = st.sampled_from(length_units)
)
def test_round_trip_conversion(amount: float, unit1: st, unit2: st):
    """ 
    Property: if unit1 can convert unit2, AND unit2 can convert back to unit1,
              then (amount -> unit2 -> unit1)  should approximately equal starting amount.
    """
    forward = answer_query((amount, unit1, unit2), graph)
    backward = None
    if forward is not None:
        backward = answer_query((forward, unit2, unit1), graph)

    # If both conversions are possible, assert roundtrip ~ identity
    if backward is not None:
        assert math.isclose(amount, backward, rel_tol=1e-3, abs_tol=1e-3)


@given(
    amount = st.floats(min_value=0.01, max_value=100.0),
    from_unit = st.sampled_from(length_units),
    to_unit = st.sampled_from(time_units)
)
def test_incompatible_units_return_none(amount: float, from_unit: st, to_unit: st):
    """ 
    Property: converting from a length unit to a time unit should always return None
            (since the clusters are disconnected) .
    """
    result = answer_query((amount, from_unit, to_unit), graph)
    assert result is None
