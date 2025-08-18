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
