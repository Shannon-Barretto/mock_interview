import unittest
from src.main import parse_facts, answer_query

class TestConversion(unittest.TestCase):
    def setUp(self):
        facts = [
            ("m", 3.28, "ft"),
            ("ft", 12, "in"),
            ("hr", 60, "min"),
            ("min", 60, "sec")
        ]
        self.graph = parse_facts(facts=facts)

    
    # -------------------------------- parse_facts tests --------------------------------
    def test_graph_builds_all_units(self):
        for unit in ["m", "ft", "in", "hr", "min", "sec"]:
            self.assertIn(unit, self.graph)


    def test_graph_build_all_units(self):
        node_m = self.graph["m"]
        node_ft = self.graph["ft"]
        self.assertTrue(any(edge.node==node_ft for edge in node_m.edges))
        self.assertTrue(any(edge.node==node_m for edge in node_ft.edges))

    def test_unrelated_units_have_no_edges(self):
        node_in = self.graph["in"]
        node_hr = self.graph["hr"]
        self.assertFalse(any(edge.node==node_hr for edge in node_in.edges))
        self.assertFalse(any(edge.node==node_in for edge in node_hr.edges))

    # -----------------------------------------------------------------------------------

    # -------------------------------- answer_query tests --------------------------------
    def test_meter_to_inch(self):
        result = answer_query((2, "m", "in"), self.graph)
        self.assertAlmostEqual(result, 78.72, places=2)

    def test_inch_to_meter(self):
        result = answer_query((13, "in", "m"), self.graph)
        self.assertAlmostEqual(result, 0.33, places=2)

    def test_no_path_between_nodes(self):
        # Should not convert "in" (inches) to "hr" (time)
        result = answer_query((13, "in", "hr"), self.graph)
        self.assertIsNone(result)

    def test_query_with_unknown_unit(self):
        result = answer_query((5, "kg", "m"), self.graph)
        self.assertIsNone(result)

    # ------------------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
