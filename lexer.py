from dataclasses import dataclass

KEYWORDS = {"let", "if", "else", "while", "fn", "return", "true", "false", "print"}
TWO_CHAR = {"==", "!=", "<=", ">=", "->"}
ONE_CHAR = set("+-*/%<>=(){}[],;:")

@dataclass(frozen=True)
class Token:
    kind: str
    value: str
    line: int
    column: int

def tokenize(source: str):
    out, i, line, col = [], 0, 1, 1
    while i < len(source):
        c = source[i]
        if c in " \t\r":
            i += 1; col += 1; continue
        if c == "\n":
            i += 1; line += 1; col = 1; continue
        if source.startswith("//", i):
            while i < len(source) and source[i] != "\n":
                i += 1; col += 1
            continue
        start_line, start_col = line, col
        if c.isalpha() or c == "_":
            j = i
            while j < len(source) and (source[j].isalnum() or source[j] == "_"): j += 1
            v = source[i:j]; kind = "KW" if v in KEYWORDS else "IDENT"
            out.append(Token(kind, v, line, col)); col += j-i; i = j; continue
        if c.isdigit():
            j = i
            while j < len(source) and (source[j].isdigit() or source[j] == "."): j += 1
            out.append(Token("NUMBER", source[i:j], line, col)); col += j-i; i = j; continue
        if c in "\"'":
            q = c; i += 1; col += 1; chars = []
            while i < len(source) and source[i] != q:
                if source[i] == "\\" and i+1 < len(source):
                    esc = source[i+1]; chars.append({"n":"\n","t":"\t","r":"\r"}.get(esc, esc))
                    i += 2; col += 2
                else:
                    chars.append(source[i]); i += 1; col += 1
            if i >= len(source): raise SyntaxError(f"Unterminated string at {start_line}:{start_col}")
            i += 1; col += 1
            out.append(Token("STRING", "".join(chars), start_line, start_col)); continue
        two = source[i:i+2]
        if two in TWO_CHAR:
            out.append(Token("OP", two, line, col)); i += 2; col += 2; continue
        if c in ONE_CHAR:
            out.append(Token("OP", c, line, col)); i += 1; col += 1; continue
        raise SyntaxError(f"Unexpected character {c!r} at {line}:{col}")
    out.append(Token("EOF", "", line, col))
    return out
