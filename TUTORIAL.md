# Thanvi Programming Language Tutorial

Welcome to **Thanvi Programming Language**.

Thanvi is an independent programming-language project created by **Meeravali Velupuri**. The reference implementation is written in Python, while Thanvi programs use their own readable syntax.

## 1. First program

```thanvi
show "Hello, Thanvi!"
finish
```

## 2. Variables

Use `set` to create a variable:

```thanvi
set name = "Meeravali"
set age = 20
show name
show age
finish
```

## 3. Conditions

Use `check`, `otherwise`, and `end`:

```thanvi
set age = 20

check age >= 18 =>
    show "Welcome, Meeravali!"
otherwise =>
    show "Access denied"
end

finish
```

## 4. Functions

Use `define` and `give`:

```thanvi
define greet(name) =>
    show "Hello, " + name
    give name
end

set result = greet("Meeravali")
show result
finish
```

## 5. Repeat

```thanvi
set count = 1

repeat count <= 3 =>
    show count
    set count = count + 1
end

finish
```

## 6. Operators

Thanvi supports:

```text
+  -  *  /  %
== != < <= > >=
```

## 7. Keywords

```text
set       variable assignment
show      output
check     condition
otherwise alternative condition branch
repeat    loop
 define   function declaration
give      function return
end       close a block
finish    end the program
true      boolean true
false     boolean false
```
