# Thanvi Programming Language

Thanvi is an independent programming-language project created by **Meeravali Velupuri**.

## v0.1.0

This repository is a complete **reference implementation** created from scratch for the initial Thanvi release. It includes a lexer, parser, AST, interpreter, CLI, tests, examples, documentation, and GitHub project files.

### Implemented in this release

- Variables with `let`
- Numbers, strings, and booleans
- Arithmetic and comparison operators
- `if` / `else`
- `while`
- Functions and `return`
- Command-line execution
- Basic error handling

## Run

Python 3.10+ is recommended.

```bash
python -m pip install -r requirements.txt
python -m thanvi.cli examples/hello.tvl
```

## Tests

```bash
pytest -q
```

## Project

GitHub organization: Thanvi  
Repository: ThanviLang

## License

MIT License

Copyright (c) 2026 Meeravali Velupuri
