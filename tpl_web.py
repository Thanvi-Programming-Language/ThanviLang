"""TPL Web v0.3 compiler: Thanvi Web syntax -> standalone HTML."""

from __future__ import annotations
import html
import json
import re
from pathlib import Path


class TPLWebError(Exception):
    pass


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def quoted(value: str) -> str:
    value = value.strip()
    if len(value) < 2 or value[0] != '"' or value[-1] != '"':
        raise TPLWebError(f"Expected quoted text, got {value!r}")
    return value[1:-1].replace('\\"', '"').replace("\\n", "\n")


def lines(source: str):
    out = []
    for n, raw in enumerate(source.splitlines(), 1):
        s = raw.strip()
        if s and not s.startswith("//"):
            out.append((n, s))
    return out


def block_end(items, start):
    depth = 1
    for i in range(start, len(items)):
        s = items[i][1]
        if re.match(r"^(page|section|button)\b", s):
            depth += 1
        elif s == "end":
            depth -= 1
            if depth == 0:
                return i
    raise TPLWebError(f"Line {items[start - 1][0] if start else 1}: missing end")


def compile_web(source: str) -> str:
    items = lines(source)
    if not items:
        raise TPLWebError("No TPL Web code found")

    n, first = items[0]
    m = re.fullmatch(r'website\s+"([^"]+)"', first)
    if not m:
        raise TPLWebError(f'Line {n}: first line must be website "Name"')

    site = m.group(1)
    html_body = []
    i = 1
    pages = 0

    while i < len(items):
        n, s = items[i]
        if s == "finish":
            if i + 1 != len(items):
                raise TPLWebError(f"Line {items[i + 1][0]}: nothing is allowed after finish")
            break

        m = re.fullmatch(r'page\s+"([^"]+)"\s*=>', s)
        if not m:
            raise TPLWebError(f'Line {n}: expected page "Name" =>')

        end = block_end(items, i + 1)
        pages += 1
        html_body.append(f'<section class="tpl-page"><div class="tpl-page-title">{esc(m.group(1))}</div>')

        j = i + 1
        while j < end:
            ln, item = items[j]

            m = re.fullmatch(r'heading\s+"(.*)"', item)
            if m:
                html_body.append(f'<h1>{esc(quoted(chr(34)+m.group(1)+chr(34)))}</h1>')
                j += 1
                continue

            m = re.fullmatch(r'text\s+"(.*)"', item)
            if m:
                html_body.append(f'<p>{esc(quoted(chr(34)+m.group(1)+chr(34)))}</p>')
                j += 1
                continue

            m = re.fullmatch(r'link\s+"([^"]+)"\s+to\s+"([^"]+)"', item)
            if m:
                label, url = m.groups()
                html_body.append(
                    f'<a class="tpl-link" href="{esc(url)}" target="_blank" rel="noopener">'
                    f'{esc(label)}</a>'
                )
                j += 1
                continue

            m = re.fullmatch(r'image\s+"([^"]+)"', item)
            if m:
                html_body.append(
                    f'<img class="tpl-image" src="{esc(m.group(1))}" alt="TPL image">'
                )
                j += 1
                continue

            m = re.fullmatch(r'section\s+"([^"]+)"\s*=>', item)
            if m:
                section_end = block_end(items, j + 1)
                html_body.append(f'<div class="tpl-section"><h3>{esc(m.group(1))}</h3>')
                k = j + 1
                while k < section_end:
                    sn, child = items[k]
                    cm = re.fullmatch(r'text\s+"(.*)"', child)
                    if not cm:
                        raise TPLWebError(
                            f"Line {sn}: section currently supports text only"
                        )
                    html_body.append(
                        f'<p>{esc(quoted(chr(34)+cm.group(1)+chr(34)))}</p>'
                    )
                    k += 1
                html_body.append("</div>")
                j = section_end + 1
                continue

            m = re.fullmatch(r'button\s+"([^"]+)"\s*=>', item)
            if m:
                button_end = block_end(items, j + 1)
                messages = []
                k = j + 1
                while k < button_end:
                    bm = re.fullmatch(r'show\s+"(.*)"', items[k][1])
                    if not bm:
                        raise TPLWebError(
                            f'Line {items[k][0]}: button currently supports show "message"'
                        )
                    messages.append(quoted(chr(34)+bm.group(1)+chr(34)))
                    k += 1
                html_body.append(
                    f'<button class="tpl-button" '
                    f'onclick="alert({json.dumps(chr(10).join(messages))})">'
                    f'{esc(m.group(1))}</button>'
                )
                j = button_end + 1
                continue

            raise TPLWebError(f"Line {ln}: unknown TPL Web syntax: {item}")

        html_body.append("</section>")
        i = end + 1

    if pages == 0:
        raise TPLWebError("A website needs at least one page")

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(site)}</title>
<style>
*{{box-sizing:border-box}}
body{{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
background:#f4f6ff;color:#202124}}
.tpl-nav{{padding:22px 28px;color:white;background:linear-gradient(135deg,#667eea,#764ba2);
font-size:25px;font-weight:800}}
.tpl-main{{max-width:960px;margin:auto;padding:32px 18px}}
.tpl-page{{background:white;border-radius:18px;padding:30px;margin-bottom:22px;
box-shadow:0 8px 30px rgba(0,0,0,.10)}}
.tpl-page-title{{font-size:14px;text-transform:uppercase;letter-spacing:.08em;
opacity:.55;margin-bottom:18px}}
.tpl-page h1{{font-size:40px;margin:0 0 12px}}
.tpl-page p{{font-size:17px;line-height:1.7;color:#555}}
.tpl-button,.tpl-link{{display:inline-block;margin:8px 8px 8px 0;padding:12px 18px;
border-radius:10px;font-weight:700;text-decoration:none}}
.tpl-button{{border:0;background:#667eea;color:white;cursor:pointer;font-size:16px}}
.tpl-link{{background:#eee;color:#333}}
.tpl-image{{max-width:100%;border-radius:14px;margin:10px 0}}
.tpl-section{{margin-top:18px;padding:18px;border-radius:12px;background:#f7f7fb}}
.tpl-section h3{{margin-top:0}}
</style>
</head>
<body>
<header class="tpl-nav">{esc(site)}</header>
<main class="tpl-main">{''.join(html_body)}</main>
</body>
</html>
"""


def compile_file(input_path: str, output_path: str = "website.html"):
    source = Path(input_path).read_text(encoding="utf-8")
    Path(output_path).write_text(compile_web(source), encoding="utf-8")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(prog="thanvi-web")
    ap.add_argument("file")
    ap.add_argument("-o", "--output", default="website.html")
    args = ap.parse_args()
    try:
        compile_file(args.file, args.output)
        print(f"TPL Web compiled successfully: {args.output}")
    except TPLWebError as exc:
        raise SystemExit(f"TPL Web error: {exc}")
