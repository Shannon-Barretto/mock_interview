from hypothesis import given, strategies as st
from collections import deque
import math

from src.main import parse_facts, answer_query

# Strategy to generate random edges between unit names
# Short random strings like "a", "xy"
unit_names = st.text(min_size=1, max_size=3)     

edge_strategy = st.tuples(
    unit_names,                                     # Left unit
    st.floats(min_value=0.1, max_value=10.0),       # multiplier
    unit_names                                      # right unit
).filter(lambda t: t[0] != t[2])                    # To avoid self loops

@given(
        facts = st.lists(edge_strategy, min_size=2, max_size=10),
        data = st.data()
)
def test_answer_query_respects_connectivity(facts, data):
    graph = parse_facts(facts=facts)

    units = list(graph.keys())
    if len(units)<2:
        # We could get [("x", 2, "y"), ("y", 3, "x")] or reverse
        return 
    
    # Draw two units from the generated graph
    unit1, unit2 = data.draw(st.sampled_from(units)), data.draw(st.sampled_from(units))

    # Manual bfs to check connectivity from unit1 -> unit2
    visited = set()
    queue = deque()
    visited.add(unit1)
    queue.append((graph[unit1], unit1))
    connected = False

    while queue:
        curreent_node, current_name = queue.popleft()
        if current_name == unit2:
            connected = True
            break
        for edge in curreent_node.edges:
            next_node = edge.node
            next_name = next_node.unit
            if next_name not in visited:
                visited.add(next_name)
                queue.append((next_node, next_name))

    result = answer_query((1.0, unit1, unit2), graph)

    if connected:
        assert result is not None
    else:
        assert result is None

# If conversion is possible in both directions between two units, the
# answer_query(a->b) * answer_query(b->a) ~ 1
@given(
    facts = st.lists(edge_strategy, min_size=2, max_size=10),
    data = st.data()
)
def test_symmetry_reciprocal(facts, data):
    graph = parse_facts(facts=facts)
    units = list(graph.keys())

    if len(units)<2:
        # We could get [("x", 2, "y"), ("y", 3, "x")] or reverse
        return
    
    unit1, unit2 = data.draw(st.sampled_from(units)), data.draw(st.sampled_from(units))

    fwd = answer_query((1.0, unit1, unit2), graph)
    back = answer_query((1.0, unit2, unit1), graph)

    # If both directions are convertible -> product shold be ~1
    if fwd is not None and back is not None:
        assert math.isclose(fwd * back, 1.0, rel_tol=1e-3, abs_tol=1e-3)
    

# If unit1 -> unit2 and unit2 -> unit3 are both reachabe, then unit1 -> unit3 should be
# reachable and answer_query(unit1->unit3) ~ answer_query(unit1->unit2) * answer_query(unit2->unit3)
@given(
    facts = st.lists(edge_strategy, min_size=3, max_size=12),
    data = st.data()
)
def test_composition_transitivity(facts, data):
    graph = parse_facts(facts=facts)
    units = list(graph.keys())

    if len(units)<2:
        # We could get [("x", 2, "y"), ("y", 3, "x")] or reverse
        return
    
    unit1 = data.draw(st.sampled_from(units))
    unit2 = data.draw(st.sampled_from(units))
    unit3 = data.draw(st.sampled_from(units))

    ab = answer_query((1.0, unit1, unit2), graph)
    bc = answer_query((1.0, unit2, unit3), graph)
    ac = answer_query((1.0, unit1, unit3), graph)

    if ab is not None and bc is not None:
        # Then ac should exist and should match teh product
        assert ac is not None
        assert math.isclose(ab * bc, ac, rel_tol=1e-3, abs_tol=1e-3)


# Test which create two separate clusters on purpose to ensure the system never
# converts across them
@given(
    amount = st.floats(min_value=0.01, max_value=100.0)
)
def test_never_connects_between_explicit_clusters(amount):
    # Manually create two clusters
    facts = [
        ("a", 2, "b"),          # Cluster 1
        ("b", 5, "c"),
        ("x", 3, "y"),           # Cluster 2
        ("y", 7, "z")
    ]
    graph = parse_facts(facts=facts)

    # e.g. try to convert from "a" to "x"
    result = answer_query((amount, "a", "x"), graph)
    assert result is None
