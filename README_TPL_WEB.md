# Thanvi TPL Web v0.3

This adds a first Web DSL to Thanvi without changing the existing v0.2 language.

## TPL Web syntax

```thanvi
website "Thanvi"

page "Home" =>
    heading "Welcome to Thanvi"
    text "This page is written in TPL."

    button "Get Started" =>
        show "Hello from TPL Web!"
    end

    link "Thanvi GitHub" to "https://github.com/Thanvi-Programming-Language/ThanviLang"
end

finish
```

## Compile

```bash
python tpl_web.py examples/website.thanvi -o website.html
```

Then open `website.html` in a browser.

## Supported Web commands

- `website "Name"`
- `page "Name" => ... end`
- `heading "Text"`
- `text "Text"`
- `button "Label" => show "Message" end`
- `link "Label" to "URL"`
- `image "URL"`
- `section "Name" => text "..." end`
- `finish`

The existing core TPL v0.2 syntax remains unchanged.
