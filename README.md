# Unit Conversion Graph – Jane Street Mock Interview

This is a small graph-based solution to convert between units (e.g. meters → inches) based on example "facts" provided, similar to a Jane Street interview question.

Conversions are treated as edges in a bidirectional graph, and queries traverse the graph to check if two units are connected and compute the conversion factor if so.

---

## 📁 Project Structure

```bash
├── src/
│   ├── edge.py                   
│   ├── node.py                    
│   ├── main.py                                           # Contains parse_facts() and answer_query()
├── tests/
│   ├── test_conversion_unittest.py                       # Traditional unnitest test
│   ├── test_conversion_pytest.py                         # Equivalent pytest tests
│   ├── test_conversion_hypothesis.py                     # Property based test with Hypothesis
│   ├── test_conversion_random_hypothesis.py              # Random graph generation + connectivity tests
```

## 🚀 How to Run

### ✅ Using `unittest`
```bash
python -m unittest discover -s tests -q
```

### ✅ Using `pytest`
```bash
pip install pytest

# verbose output
python -m pytest -v

# quite mode
python -m pytest -q
```

### ✅ Using `hypothesis` (Property based testing)
```bash
pip install hypothesis

# run only Hypothesis test
python -m pytest -v tests/test_conversion_hypothesis.py
python -m pytest -v tests/test_conversion_random_hypothesis.py

# Or run everything (unit, pytest and hypothesis)
python -m pytest -v
```

## 🧪 Example Facts + Queries
```bash
Facts:
    m = 3.28 ft
    ft = 12 in
    hr = 60 min
    min = 60 sec

Queries:
    2 m = ? in   -> 78.72
    13 in = ? m  -> 0.33
    13 in = ? hr -> not convertible
```

## 🧪 Property-Based Tests with Hypothesis

Instead of writing only fixed cases, we use [Hypothesis](https://hypothesis.readthedocs.io/en/latest/tutorial/introduction.html) to automatically generate thousands of random scenarios anc check that core principles always hold.

Some properties tested:
- **Round-trip conversions:** Converting `x` from unit A -> B -> A shuld give back approximately `x`.
- **Connectivity:** If two units are connected in a graoh, then a conversion should exist.
- **Symmetry:** If A converts to B and B converts to C, then A should ocnvert to C.
- **Composition:** If A converts to B and B converts to C, tehn A should convert to C.
- **Disconnected clusters:** Queries across disconnected subgraphs shuld return "not convertible"

This ensure that the graph based conversion system behaves correctly not just for a few examples, but for a wide range of automatically generated cases.
