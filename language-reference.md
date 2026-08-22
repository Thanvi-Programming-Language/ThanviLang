# Thanvi Language Reference — v0.2.0

Thanvi uses a simple, readable syntax.

## Variables

```thanvi
set name = "Thanvi"
set age = 20
```

## Output

```thanvi
show "Hello, Thanvi!"
show name
```

## Conditions

```thanvi
check age >= 18 =>
    show "Adult"
otherwise =>
    show "Minor"
end
```

## Repeat loops

```thanvi
set count = 1
repeat count <= 3 =>
    show count
    set count = count + 1
end
```

## Functions

```thanvi
define add(a, b) =>
    give a + b
end

show add(2, 3)
```

## Program ending

`finish` marks the end of a Thanvi program.

```thanvi
finish
```

## Comments

Use `//` for comments.

```thanvi
// This is a Thanvi comment
show "Hello"
finish
```
