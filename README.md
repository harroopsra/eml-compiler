# EML Compiler

Compile any ordinary math expression into **EML** (Exp‑Minus‑Log) — a language with a single binary operator.

This is based on Andrzej Odrzywolek's paper [*All elementary functions from a single binary operator*](https://arxiv.org/abs/2603.21852): the operator

```
eml(x, y) = exp(x) − ln(y)
```

together with the constant `1` can express everything a scientific calculator can — addition, subtraction, multiplication, division, powers, roots, logarithms, `π`, `e`, and more. Every compiled expression becomes a binary tree of identical nodes, with a grammar as simple as:

```
S → 1 | eml(S, S) | variable
```

For example, the paper's identity for the natural log:

```
ln(x) = eml(1, eml(eml(1, x), 1))
```

This project turns human-readable math into those trees, serves them over an API, and quizzes you on the results.

## Examples

| Input | EML |
|---|---|
| `1` | `1` |
| `e` | `EML[1,1]` |
| `exp(x)` | `EML[x,1]` |
| `ln(x)` | `EML[1,EML[EML[1,x],1]]` |
| `x + y` | `EML[EML[1,EML[EML[1,x],1]],EML[EML[EML[1,EML[EML[1,EML[1,EML[EML[1,1],1]]],1]],EML[y,1]],1]]` |

Yes, expressions grow fast — `2` is already 92 characters, and `sqrt(x)` is 484. That's the point: everything is built from one operator and the constant `1`. Integers are made by counting: `1`, `eml_add(1, 1)`, …

## What's in here

| File | What it does |
|---|---|
| `compiler_v7.py` | The compiler. Parses human-readable math with [SymPy](https://www.sympy.org), emits EML strings. |
| `main.py` | FastAPI service: generates random expressions paired with their compiled EML forms. |
| `test.html` | The quiz game (D3): "Which one of these EML trees is `(inv1)*(invpi)-e`?" |

## Quickstart

```bash
git clone https://github.com/harroopsra/eml-compiler.git
cd eml-compiler
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# run the quiz API
uvicorn main:app --port 8000
```

Then open `test.html` in a browser — it fetches from `http://127.0.0.1:8000`.

## Using the compiler directly

```python
from compiler_v7 import eml_compile_from_string

eml_compile_from_string("exp(x)")   # 'EML[x,1]'
eml_compile_from_string("ln(x)")    # 'EML[1,EML[EML[1,x],1]]'
```

Run its built-in test suite with:

```bash
python compiler_v7.py
```

### Supported input syntax

- **Operators:** `+`, `-`, `*`, `/`, `^` (or `**`), parentheses
- **Functions:** `exp`, `ln` (or `log`), `sqrt`, `square`, `inv`, `avg`, `hypot`, `sigma` (logistic sigmoid)
- **Constants:** `e`, `pi`
- **Anything else** is treated as a variable (`x`, `y`, `theta`, …)

## Credits

- The math: Andrzej Odrzywolek, *[All elementary functions from a single binary operator](https://arxiv.org/abs/2603.21852)* (arXiv:2603.21852). The operator and its identities are his discovery, found by systematic exhaustive search.
- The code: built over a hackathon weekend with Simon.

## License

MIT
