# Unit Conversion Graph – Jane Street Mock Interview

This is a small graph-based solution to convert between units (e.g. meters → inches) based on example "facts" provided, similar to a Jane Street interview question.

Conversions are treated as edges in a bidirectional graph, and queries traverse the graph to check if two units are connected and compute the conversion factor if so.

---

## 📁 Project Structure

```bash
├── src/
│   ├── edge.py                   
│   ├── node.py                    
│   ├── main.py                               # Contains parse_facts() and answer_query()
├── tests/
│   ├── test_conversion_unittest.py                  
│   ├── test_conversion_pytest.py
```

## 🚀 How to Run

### ✅ Using `unittest`
```bash
python3 -m unittest discover -s tests -q
```

### ✅ Using `pytest`
```bash
pip install pytest

# verbose output
python3 -m pytest -v

# quite mode
python3 -m pytest -q
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
