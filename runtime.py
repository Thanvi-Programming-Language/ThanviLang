from parser import *
class ReturnSignal(Exception):
 def __init__(self,v):self.value=v
class FinishSignal(Exception):pass
class FunctionValue:
 def __init__(self,stmt,closure,rt):self.stmt=stmt;self.closure=closure.copy();self.rt=rt
 def __call__(self,args):
  if len(args)!=len(self.stmt.params):raise RuntimeError(f'{self.stmt.name}() expects {len(self.stmt.params)} argument(s), got {len(args)}')
  e=self.closure.copy();e.update(zip(self.stmt.params,args))
  try:self.rt.block(self.stmt.body,e)
  except ReturnSignal as r:return r.value
  return None
class Runtime:
 def __init__(self,loop_limit=10000):self.output=[];self.functions={};self.loop_limit=loop_limit
 def ev(self,n,e):
  if isinstance(n,Literal):
   return [self.ev(x,e) for x in n.value] if isinstance(n.value,list) else n.value
  if isinstance(n,Name):
   if n.value in e:return e[n.value]
   raise RuntimeError('Undefined variable: '+n.value)
  if isinstance(n,Index):
   o=self.ev(n.obj,e);k=self.ev(n.key,e)
   try:return o[int(k)] if isinstance(o,list) else o[k]
   except Exception as x:raise RuntimeError('Index error: '+str(x))
  if isinstance(n,Unary):
   v=self.ev(n.expr,e);return -v if n.op=='-' else not bool(v)
  if isinstance(n,Binary):
   if n.op=='and':return bool(self.ev(n.left,e)) and bool(self.ev(n.right,e))
   if n.op=='or':return bool(self.ev(n.left,e)) or bool(self.ev(n.right,e))
   a=self.ev(n.left,e);b=self.ev(n.right,e)
   if n.op=='+':return str(a)+str(b) if isinstance(a,str) or isinstance(b,str) else a+b
   if n.op=='-':return a-b
   if n.op=='*':return a*b
   if n.op=='/':
    if b==0:raise RuntimeError('Division by zero')
    return a/b
   if n.op=='%':return a%b
   return {'==':a==b,'!=':a!=b,'<':a<b,'>':a>b,'<=':a<=b,'>=':a>=b}[n.op]
  if isinstance(n,Call):
   a=[self.ev(x,e) for x in n.args]
   b={'len':len,'str':str,'num':lambda x:float(x) if '.' in str(x) else int(x),'type':lambda x:type(x).__name__,'abs':abs,'round':round,'min':min,'max':max}
   if n.name in b:return b[n.name](*a)
   if n.name in self.functions:return self.functions[n.name](a)
   raise RuntimeError('Undefined function: '+n.name)
  raise RuntimeError('Unknown expression')
 def stmt(self,s,e):
  try:
   if isinstance(s,SetStmt):e[s.name]=self.ev(s.expr,e)
   elif isinstance(s,ShowStmt):self.output.append(str(self.ev(s.expr,e)))
   elif isinstance(s,ExprStmt):self.ev(s.expr,e)
   elif isinstance(s,GiveStmt):raise ReturnSignal(self.ev(s.expr,e))
   elif isinstance(s,FinishStmt):raise FinishSignal()
   elif isinstance(s,FunctionStmt):self.functions[s.name]=FunctionValue(s,e,self)
   elif isinstance(s,CheckStmt):self.block(s.yes if bool(self.ev(s.cond,e)) else s.no,e)
   elif isinstance(s,RepeatStmt):
    n=0
    while bool(self.ev(s.cond,e)):
     n+=1
     if n>self.loop_limit:raise RuntimeError(f'Loop limit exceeded ({self.loop_limit})')
     self.block(s.body,e)
  except (ReturnSignal,FinishSignal):raise
  except Exception as x:
   if str(x).startswith('Line '):raise
   raise RuntimeError(f'Line {s.line}: {x}')
 def block(self,b,e):
  for s in b:self.stmt(s,e)
 def run(self,source):
  try:self.block(parse(source).body,{})
  except FinishSignal:pass
  return '\n'.join(self.output)
def run(source):return Runtime().run(source)
