from dataclasses import dataclass
from lexer import lex
@dataclass
class Program: body:list
@dataclass
class SetStmt: name:str;expr:object;line:int
@dataclass
class ShowStmt: expr:object;line:int
@dataclass
class CheckStmt: cond:object;yes:list;no:list;line:int
@dataclass
class RepeatStmt: cond:object;body:list;line:int
@dataclass
class FunctionStmt: name:str;params:list;body:list;line:int
@dataclass
class GiveStmt: expr:object;line:int
@dataclass
class FinishStmt: line:int
@dataclass
class ExprStmt: expr:object;line:int
@dataclass
class Literal: value:object
@dataclass
class Name: value:str
@dataclass
class Unary: op:str;expr:object
@dataclass
class Binary: left:object;op:str;right:object
@dataclass
class Call: name:str;args:list
@dataclass
class Index: obj:object;key:object
class Parser:
 def __init__(self,s):self.t=lex(s);self.i=0
 def val(self):return self.t[self.i].value
 def take(self,v=None):
  t=self.t[self.i]
  if v is not None and t.value!=v:raise SyntaxError(f'Line {t.line}: expected {v!r}, got {t.value!r}')
  self.i+=1;return t
 def program(self):
  b=[]
  while self.t[self.i].kind!='EOF':b.append(self.statement())
  return Program(b)
 def statement(self):
  t=self.t[self.i];v=t.value
  if v=='set':self.take();n=self.take().value;self.take('=');return SetStmt(n,self.expr(),t.line)
  if v=='show':self.take();return ShowStmt(self.expr(),t.line)
  if v=='check':
   self.take();c=self.expr();self.take('=>');yes=self.block({'otherwise','end'});no=[]
   if self.val()=='otherwise':self.take();self.take('=>');no=self.block({'end'})
   self.take('end');return CheckStmt(c,yes,no,t.line)
  if v=='repeat':
   self.take();c=self.expr();self.take('=>');b=self.block({'end'});self.take('end');return RepeatStmt(c,b,t.line)
  if v=='define':
   self.take();n=self.take().value;self.take('(');p=[]
   if self.val()!=')':
    while True:
     p.append(self.take().value)
     if self.val()!=',':break
     self.take(',')
   self.take(')');self.take('=>');b=self.block({'end'});self.take('end');return FunctionStmt(n,p,b,t.line)
  if v=='give':self.take();return GiveStmt(self.expr(),t.line)
  if v=='finish':self.take();return FinishStmt(t.line)
  if v in ('end','otherwise'):raise SyntaxError(f'Line {t.line}: unexpected {v!r}')
  return ExprStmt(self.expr(),t.line)
 def block(self,stops):
  b=[]
  while self.t[self.i].kind!='EOF' and self.val() not in stops:b.append(self.statement())
  return b
 def expr(self):return self.logic_or()
 def logic_or(self):
  x=self.logic_and()
  while self.val()=='or':self.take();x=Binary(x,'or',self.logic_and())
  return x
 def logic_and(self):
  x=self.compare()
  while self.val()=='and':self.take();x=Binary(x,'and',self.compare())
  return x
 def compare(self):
  x=self.add()
  while self.val() in ('==','!=','<','>','<=','>='):
   o=self.take().value;x=Binary(x,o,self.add())
  return x
 def add(self):
  x=self.mul()
  while self.val() in ('+','-'):
   o=self.take().value;x=Binary(x,o,self.mul())
  return x
 def mul(self):
  x=self.unary()
  while self.val() in ('*','/','%'):
   o=self.take().value;x=Binary(x,o,self.unary())
  return x
 def unary(self):
  if self.val() in ('-','not'):
   o=self.take().value;return Unary(o,self.unary())
  return self.primary()
 def primary(self):
  t=self.t[self.i]
  if t.kind in ('NUMBER','STRING'):self.i+=1;x=Literal(t.value)
  elif t.value in ('true','false'):self.i+=1;x=Literal(t.value=='true')
  elif t.kind=='IDENT':
   self.i+=1
   if self.val()=='(':
    self.take('(');a=[]
    if self.val()!=')':
     while True:
      a.append(self.expr())
      if self.val()!=',':break
      self.take(',')
    self.take(')');x=Call(t.value,a)
   else:x=Name(t.value)
  elif t.value=='[':
   self.take();a=[]
   if self.val()!=']':
    while True:
     a.append(self.expr())
     if self.val()!=',':break
     self.take(',')
   self.take(']');x=Literal(a)
  elif t.value=='(':
   self.take();x=self.expr();self.take(')')
  else:raise SyntaxError(f'Line {t.line}: expected expression')
  while self.val()=='[':
   self.take();k=self.expr();self.take(']');x=Index(x,k)
  return x
def parse(s):return Parser(s).program()
