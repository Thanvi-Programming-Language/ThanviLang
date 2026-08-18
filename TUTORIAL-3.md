# Thanvi Programming Language Tutorial

Welcome to the **Thanvi Programming Language**.

Thanvi is an independent programming-language project created by Meeravali Velpuri.

This tutorial introduces the syntax currently demonstrated by the ThanviLang v0.1.0 project.

---

## 1. About Thanvi

ThanviLang is a programming language implementation written in Python.

The v0.1.0 project includes:

- Lexer
- Parser
- AST
- Interpreter/runtime
- Command-line execution
- Tests
- Language documentation

The current documented implementation includes variables, numbers, strings, booleans, arithmetic and comparison operators, `if / else`, `while`, functions, `return`, command-line execution, and basic error handling.

---

# 2. Your First Thanvi Program

A simple Thanvi program can print a value:

```thanvi
print 2 + 3 * 4;
```

The expected result is:

```text
14
```

Save your Thanvi source code in a file and run it using the Thanvi command-line interface described in the project README.

---

# 3. Variables

Thanvi uses `let` to create variables.

```thanvi
let x = 1;
```

A variable can then be used in an expression:

```thanvi
let x = 10;
print x;
```

Variables can store values such as numbers, strings, and booleans.

---

# 4. Numbers

Thanvi supports numeric values and arithmetic expressions.

Example:

```thanvi
print 2 + 3;
```

Arithmetic operators include:

```text
+
-
*
/
```

Example:

```thanvi
print 10 + 5;
print 10 - 5;
print 10 * 5;
print 10 / 5;
```

Expressions can contain multiple operators:

```thanvi
print 2 + 3 * 4;
```

---

# 5. Strings

Strings can be written inside quotation marks.

Example:

```thanvi
print "Hello, Thanvi!";
```

Another example:

```thanvi
let name = "Thanvi";
print name;
```

---

# 6. Boolean Values

Thanvi supports boolean values.

Example:

```thanvi
let active = true;
let disabled = false;
```

Booleans can be used with conditions.

---

# 7. Comparison Operators

Thanvi supports comparison expressions.

Examples include:

```text
<
>
==
```

Example:

```thanvi
print 2 < 3;
```

A comparison produces a value that can be used by conditional logic.

---

# 8. If / Else

Use `if` to execute code when a condition is true.

Example:

```thanvi
if (2 < 3) {
    print "yes";
}
```

You can add `else` for the alternative case:

```thanvi
if (2 < 3) {
    print "yes";
} else {
    print "no";
}
```

This allows Thanvi programs to make decisions.

---

# 9. While Loops

Thanvi supports `while` loops.

Basic structure:

```thanvi
while (condition) {
    // statements
}
```

A `while` loop repeatedly executes its block while the condition remains true.

Use changing variables in loop conditions so that the loop can eventually stop.

---

# 10. Functions

Thanvi supports functions.

The basic function syntax is:

```thanvi
fn function_name(arguments) {
    // statements
}
```

Example:

```thanvi
fn add(a, b) {
    return a + b;
}
```

The function can then be called:

```thanvi
print add(2, 3);
```

The expected result is:

```text
5
```

---

# 11. Return

The `return` statement sends a value back from a function.

Example:

```thanvi
fn add(a, b) {
    return a + b;
}
```

Here, `a + b` is returned by the function.

---

# 12. Combining Features

Thanvi programs can combine variables, expressions, conditions, loops, and functions.

Example:

```thanvi
let x = 10;

if (x > 5) {
    print "x is greater than 5";
} else {
    print "x is 5 or less";
}
```

This demonstrates how individual Thanvi features can be combined into a program.

---

# 13. Program Structure

A Thanvi program is made from statements and expressions.

Common elements currently demonstrated by ThanviLang include:

| Feature | Syntax |
|---|---|
| Variable | `let x = 10;` |
| Print | `print x;` |
| Arithmetic | `2 + 3 * 4` |
| Comparison | `2 < 3` |
| Condition | `if (...) { ... }` |
| Alternative | `else { ... }` |
| Loop | `while (...) { ... }` |
| Function | `fn add(a, b) { ... }` |
| Return | `return a + b;` |

---

# 14. Testing Thanvi

ThanviLang includes a Python test file:

```text
test_thanvi.py
```

The project tests examples such as:

- Parser behavior
- Arithmetic and printing
- Conditions
- Functions

Example test program:

```thanvi
print 2 + 3 * 4;
```

Expected output:

```text
14
```

Function example:

```thanvi
fn add(a,b) { return a+b; }
print add(2,3);
```

Expected output:

```text
5
```

---

# 15. Error Handling

ThanviLang includes basic error handling.

When developing a Thanvi program, check the error message carefully if the interpreter cannot parse or execute your code.

For development, keep programs small and test each feature separately before combining multiple features.

---

# 16. Recommended Learning Path

If you are new to Thanvi, learn the language in this order:

### Step 1 — Print

```thanvi
print "Hello, Thanvi!";
```

### Step 2 — Variables

```thanvi
let x = 10;
print x;
```

### Step 3 — Arithmetic

```thanvi
print 2 + 3 * 4;
```

### Step 4 — Conditions

```thanvi
if (2 < 3) {
    print "yes";
} else {
    print "no";
}
```

### Step 5 — Loops

Learn `while` and practice repeating statements.

### Step 6 — Functions

```thanvi
fn add(a, b) {
    return a + b;
}

print add(2, 3);
```

### Step 7 — Build Programs

Combine variables, conditions, loops, and functions.

---

# 17. Example Program

Here is a small example combining several Thanvi features:

```thanvi
let x = 10;

if (x > 5) {
    print "Greater than 5";
} else {
    print "5 or less";
}

fn add(a, b) {
    return a + b;
}

print add(2, 3);
```

---

# 18. Project Files

Important files in the ThanviLang repository include:

```text
README.md
language-reference.md
lexer.py
parser.py
runtime.py
cli.py
test_thanvi.py
requirements.txt
```

The exact implementation details are maintained in the source files and language reference.

---

# 19. Contributing

ThanviLang is an open-source project.

Contributions can help improve:

- Language features
- Parser
- Lexer
- Runtime
- CLI
- Documentation
- Tests
- Examples

Before making changes, read the project's contribution and code-of-conduct documents.

---

# 20. Version

This tutorial documents the syntax and features demonstrated by the ThanviLang **v0.1.0** project.

As ThanviLang develops, new language features may be added.

For the latest syntax and implementation details, always check:

```text
README.md
language-reference.md
```

---

## License

ThanviLang is released under the MIT License.

Copyright (c) Meeravali Velpuri.
