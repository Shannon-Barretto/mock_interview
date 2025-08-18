""" 
example facts:
    m = 3.28 ft
    ft = 12 in
    hr = 60 min
    min = 60 sec
example queries:
    2 m = ? in ....-> answer = 78.72
    13 in = ? m....-> answer = 0.333(roughly)
    13 in = ? hr...-> "not convertible!"
"""

from src.node import Node

def parse_facts(facts: str) -> dict:
    name_to_node = {}
    for (left_unit, multiplier, right_unit) in facts:
        if left_unit not in name_to_node:
            left_node = Node(left_unit)
            name_to_node[left_unit] = left_node
        if right_unit not in name_to_node:
            right_node = Node(right_unit)
            name_to_node[right_unit] = right_node
        
        name_to_node[left_unit].add_edge(multiplier, name_to_node[right_unit])
        name_to_node[right_unit].add_edge(1/multiplier, name_to_node[left_unit])

    return name_to_node


from collections import deque

def answer_query(query: str, facts: dict) -> None:
    starting_amount, from_unit, to_unit = query
    if from_unit not in facts or to_unit not in facts:
        return None
    
    from_node = facts[from_unit]
    to_node = facts[to_unit]

    visited = set()
    to_visit = deque()
    to_visit.append((from_node, starting_amount))
    visited.add(from_node)

    while to_visit:
        current_node, current_amount = to_visit.popleft()
        if current_node == to_node:
            return current_amount
        
        for edge in current_node.edges:
            if edge.node not in visited:
                visited.add(edge.node)
                with_latest_multiplier = current_amount * edge.multiplier
                to_visit.append((edge.node, with_latest_multiplier))
    
    return None
