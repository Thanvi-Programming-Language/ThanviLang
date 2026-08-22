from dataclasses import dataclass
from lexer import tokenize

@dataclass
class Program: statements: list
@dataclass
class Set: name: str; expr: object
@dataclass
class Show: expr: object
@dataclass
class ExprStmt: expr: object
@dataclass
class Block: statements: list
@dataclass
class Check: condition: object; then: Block; otherwise: Block | None
@dataclass
class Repeat: condition: object; body: Block
@dataclass
class Function: name: str; params: list; body: Block
@dataclass
class Give: expr: object | None
@dataclass
class Finish: pass
@dataclass
class Literal: value: object
@dataclass
class Name: value: str
@dataclass
class Unary: op: str; expr: object
@dataclass
class Binary: left: object; op: str; right: object
@dataclass
class Call: callee: object; args: list


class Parser:
    def __init__(self, source):
        self.t = tokenize(source)
        self.i = 0

    def cur(self):
        return self.t[self.i]

    def take(self, value=None):
        token = self.cur()
        if value is not None and token.value != value:
            raise SyntaxError(f"Expected {value!r}, got {token.value!r} at {token.line}:{token.column}")
        self.i += 1
        return token

    def skip_newlines(self):
        while self.cur().kind == "NEWLINE" or self.cur().value == ";":
            self.i += 1

    def require_line_end(self):
        if self.cur().kind == "NEWLINE":
            self.skip_newlines()
        elif self.cur().value == ";":
            self.skip_newlines()
        elif self.cur().kind != "EOF":
            raise SyntaxError(f"Expected end of line, got {self.cur().value!r}")

    def program(self):
        statements = []
        self.skip_newlines()
        while self.cur().kind != "EOF":
            if self.cur().value == "finish":
                self.take("finish")
                self.require_line_end()
                self.skip_newlines()
                if self.cur().kind != "EOF":
                    raise SyntaxError("Nothing is allowed after finish")
                statements.append(Finish())
                break
            statements.append(self.statement())
            self.skip_newlines()
        return Program(statements)

    def statement(self):
        value = self.cur().value
        if value == "set":
            self.take("set")
            name = self.take().value
            self.take("=")
            expr = self.expr()
            self.require_line_end()
            return Set(name, expr)

        if value == "show":
            self.take("show")
            expr = self.expr()
            self.require_line_end()
            return Show(expr)

        if value == "check":
            self.take("check")
            condition = self.expr()
            self.take("=>")
            self.require_line_end()
            then = self.block_until("otherwise", "end")
            otherwise = None
            if self.cur().value == "otherwise":
                self.take("otherwise")
                self.take("=>")
                self.require_line_end()
                otherwise = self.block_until("end")
            self.take("end")
            self.require_line_end()
            return Check(condition, then, otherwise)

        if value == "repeat":
            self.take("repeat")
            condition = self.expr()
            self.take("=>")
            self.require_line_end()
            body = self.block_until("end")
            self.take("end")
            self.require_line_end()
            return Repeat(condition, body)

        if value == "define":
            self.take("define")
            name = self.take().value
            self.take("(")
            params = []
            if self.cur().value != ")":
                while True:
                    params.append(self.take().value)
                    if self.cur().value != ",":
                        break
                    self.take(",")
            self.take(")")
            self.take("=>")
            self.require_line_end()
            body = self.block_until("end")
            self.take("end")
            self.require_line_end()
            return Function(name, params, body)

        if value == "give":
            self.take("give")
            expr = None if self.cur().kind in ("NEWLINE", "EOF") or self.cur().value == ";" else self.expr()
            self.require_line_end()
            return Give(expr)

        if value == "end":
            raise SyntaxError("Unexpected 'end'")

        expr = self.expr()
        self.require_line_end()
        return ExprStmt(expr)

    def block_until(self, *terminators):
        statements = []
        self.skip_newlines()
        while self.cur().kind != "EOF" and self.cur().value not in terminators:
            statements.append(self.statement())
            self.skip_newlines()
        if self.cur().kind == "EOF":
            raise SyntaxError(f"Expected one of {terminators}, got end of file")
        return Block(statements)

    def expr(self): return self.equality()

    def equality(self):
        node = self.compare()
        while self.cur().value in ("==", "!="):
            op = self.take().value
            node = Binary(node, op, self.compare())
        return node

    def compare(self):
        node = self.term()
        while self.cur().value in ("<", "<=", ">", ">="):
            op = self.take().value
            node = Binary(node, op, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.cur().value in ("+", "-"):
            op = self.take().value
            node = Binary(node, op, self.factor())
        return node

    def factor(self):
        node = self.unary()
        while self.cur().value in ("*", "/", "%"):
            op = self.take().value
            node = Binary(node, op, self.unary())
        return node

    def unary(self):
        if self.cur().value in ("+", "-"):
            return Unary(self.take().value, self.unary())
        return self.call()

    def call(self):
        node = self.primary()
        while self.cur().value == "(":
            self.take("(")
            args = []
            if self.cur().value != ")":
                while True:
                    args.append(self.expr())
                    if self.cur().value != ",":
                        break
                    self.take(",")
            self.take(")")
            node = Call(node, args)
        return node

    def primary(self):
        token = self.take()
        if token.kind == "NUMBER":
            return Literal(float(token.value) if "." in token.value else int(token.value))
        if token.kind == "STRING":
            return Literal(token.value)
        if token.value == "true":
            return Literal(True)
        if token.value == "false":
            return Literal(False)
        if token.kind == "IDENT":
            return Name(token.value)
        if token.value == "(":
            expr = self.expr()
            self.take(")")
            return expr
        raise SyntaxError(f"Unexpected token {token.value!r} at {token.line}:{token.column}")


def parse(source):
    return Parser(source).program()
