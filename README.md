# Thanvi Programming Language v0.4.0

Advanced Web + Data Edition.

Creator: Meeravali Velupuri

## Highlights
- Variables, output, conditions, loops and functions
- Arrays and indexing
- `and`, `or`, `not`
- Built-ins: `len`, `str`, `num`, `type`, `abs`, `round`, `min`, `max`
- Comments with `#` or `//`
- Line-aware runtime errors
- Loop safety limit
- TPL Web compiler
- Standalone HTML output
- Browser playground

## Run
```bash
python cli.py examples/hello.thanvi
python cli.py examples/data.thanvi
python cli.py examples/web.thanvi --web -o website.html
```

## TPL Web
```thanvi
website "Thanvi 0.4.0"

page "Home" =>
    heading "Welcome to Thanvi"
    text "This website is generated with TPL Web."

    section "Features" =>
        text "Readable syntax"
        text "Arrays and functions"
        text "Standalone HTML"
    end

    button "Start" =>
        show "Welcome!"
    end
end

finish
```

This is a development release. Test it before treating it as an official production compiler.
