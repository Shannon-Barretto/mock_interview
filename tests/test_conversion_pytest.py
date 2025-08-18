import pytest
from src.main import parse_facts, answer_query

@pytest.fixture
def graph():
    facts = [
        ("m", 3.28, "ft"),
        ("ft", 12, "in"),
        ("hr", 60, "min"),
        ("min", 60, "sec")
    ]
    return parse_facts(facts=facts)

def test_graph_builds_all_units(graph: dict):
    for unit in ["m", "ft", "in", "hr", "min", "sec"]:
        assert unit in graph

def test_edges_are_bidirectional(graph: dict):
    node_m = graph["m"]
    node_ft = graph["ft"]
    assert any(edge.node==node_m for edge in node_ft.edges)
    assert any(edge.node==node_ft for edge in node_m.edges)

@pytest.mark.parametrize(
    "amount, from_unit, to_unit, expected",
    [
        (2, "m", "in", 78.72),
        (13, "in", "m", 0.33)
    ]
)

def test_valid_conversations(graph: dict, amount: int, from_unit: str, to_unit: str, expected: int):
    result = answer_query((amount, from_unit, to_unit), graph)
    assert round(result, 2) == expected

def test_incompatible_units(graph: dict):
    result = answer_query((13, "in", "hr"), graph)
    assert result is None

def test_query_with_unknown_unit(graph: dict):
    result = answer_query((5, "kg", "m"), graph)
    assert result is None

def test_no_path_between_nodes(graph: dict):
    # Should not convert "in" (inches) to "hr" (time)
    result = answer_query((1, "in", "hr"), graph)
    assert result is None
