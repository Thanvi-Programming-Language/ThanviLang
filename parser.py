from dataclasses import dataclass
from lexer import tokenize

@dataclass
class Program: statements: list
@dataclass
class Let: name: str; expr: object
@dataclass
class Print: expr: object
@dataclass
class ExprStmt: expr: object
@dataclass
class Block: statements: list
@dataclass
class If: condition: object; then: Block; otherwise: Block|None
@dataclass
class While: condition: object; body: Block
@dataclass
class Function: name: str; params: list; body: Block
@dataclass
class Return: expr: object|None
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
        self.t = tokenize(source); self.i = 0
    def cur(self): return self.t[self.i]
    def take(self, value=None):
        x = self.cur()
        if value is not None and x.value != value: raise SyntaxError(f"Expected {value!r}, got {x.value!r}")
        self.i += 1; return x
    def program(self):
        s=[]
        while self.cur().kind != "EOF": s.append(self.statement())
        return Program(s)
    def statement(self):
        if self.cur().value == "let":
            self.take(); name=self.take().value; self.take("="); e=self.expr(); self.take(";"); return Let(name,e)
        if self.cur().value == "print":
            self.take(); e=self.expr(); self.take(";"); return Print(e)
        if self.cur().value == "if":
            self.take(); self.take("("); c=self.expr(); self.take(")"); a=self.block()
            b=None
            if self.cur().value=="else": self.take(); b=self.block()
            return If(c,a,b)
        if self.cur().value == "while":
            self.take(); self.take("("); c=self.expr(); self.take(")"); return While(c,self.block())
        if self.cur().value == "fn":
            self.take(); n=self.take().value; self.take("("); p=[]
            if self.cur().value!=")":
                while True:
                    p.append(self.take().value)
                    if self.cur().value!="," : break
                    self.take(",")
            self.take(")"); return Function(n,p,self.block())
        if self.cur().value == "return":
            self.take(); e=None if self.cur().value==";" else self.expr(); self.take(";"); return Return(e)
        e=self.expr(); self.take(";"); return ExprStmt(e)
    def block(self):
        self.take("{"); s=[]
        while self.cur().value!="}": s.append(self.statement())
        self.take("}"); return Block(s)
    def expr(self): return self.equality()
    def equality(self):
        n=self.compare()
        while self.cur().value in ("==","!="): o=self.take().value; n=Binary(n,o,self.compare())
        return n
    def compare(self):
        n=self.term()
        while self.cur().value in ("<","<=",">",">="): o=self.take().value; n=Binary(n,o,self.term())
        return n
    def term(self):
        n=self.factor()
        while self.cur().value in ("+","-"): o=self.take().value; n=Binary(n,o,self.factor())
        return n
    def factor(self):
        n=self.unary()
        while self.cur().value in ("*","/","%"): o=self.take().value; n=Binary(n,o,self.unary())
        return n
    def unary(self):
        if self.cur().value in ("+","-"): return Unary(self.take().value,self.unary())
        return self.call()
    def call(self):
        n=self.primary()
        while self.cur().value=="(":
            self.take(); a=[]
            if self.cur().value!=")":
                while True:
                    a.append(self.expr())
                    if self.cur().value!="," : break
                    self.take(",")
            self.take(")"); n=Call(n,a)
        return n
    def primary(self):
        x=self.take()
        if x.kind=="NUMBER": return Literal(float(x.value) if "." in x.value else int(x.value))
        if x.kind=="STRING": return Literal(x.value)
        if x.value=="true": return Literal(True)
        if x.value=="false": return Literal(False)
        if x.kind=="IDENT": return Name(x.value)
        if x.value=="(": e=self.expr(); self.take(")"); return e
        raise SyntaxError(f"Unexpected token {x.value!r}")

def parse(source): return Parser(source).program()
