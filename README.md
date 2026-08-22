# Thanvi Programming Language

Thanvi is an independent programming-language project created by **Meeravali Velupuri**.

## v0.2.0

This release introduces a new readable Thanvi syntax. The implementation remains Python-based, but users write programs in Thanvi's own syntax.

### Core syntax

- `set` for variables
- `show` for output
- `check` / `otherwise` / `end` for conditions
- `repeat` / `end` for loops
- `define` / `give` / `end` for functions
- `finish` for program termination
- Numbers, strings, booleans, arithmetic and comparison operators

### Example

```thanvi
set name = "Meeravali"
set age = 20

check age >= 18 =>
    show "Welcome, " + name
otherwise =>
    show "Access denied"
end

finish
```

## Run

Python 3.10+ is recommended.

```bash
python cli.py example.thanvi
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
