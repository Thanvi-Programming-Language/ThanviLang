from parser import *

class ReturnSignal(Exception):
    def __init__(self, value): self.value=value

class FunctionValue:
    def __init__(self, node, closure): self.node=node; self.closure=closure
    def __call__(self, args):
        if len(args)!=len(self.node.params): raise TypeError("wrong number of arguments")
        env=dict(self.closure)
        env.update(zip(self.node.params,args))
        try: Interpreter().exec_block(self.node.body, env)
        except ReturnSignal as r: return r.value
        return None

class Interpreter:
    def __init__(self): self.env={"print": print}
    def exec_program(self, program):
        for s in program.statements: self.exec_stmt(s,self.env)
    def exec_block(self, block, env):
        for s in block.statements: self.exec_stmt(s,env)
    def exec_stmt(self,s,env):
        if isinstance(s,Let): env[s.name]=self.eval(s.expr,env)
        elif isinstance(s,Print): print(self.eval(s.expr,env))
        elif isinstance(s,ExprStmt): self.eval(s.expr,env)
        elif isinstance(s,Block): self.exec_block(s,env)
        elif isinstance(s,If):
            if self.eval(s.condition,env): self.exec_block(s.then,env)
            elif s.otherwise: self.exec_block(s.otherwise,env)
        elif isinstance(s,While):
            guard=0
            while self.eval(s.condition,env):
                guard+=1
                if guard>1_000_000: raise RuntimeError("loop limit exceeded")
                self.exec_block(s.body,env)
        elif isinstance(s,Function): env[s.name]=FunctionValue(s,env)
        elif isinstance(s,Return): raise ReturnSignal(None if s.expr is None else self.eval(s.expr,env))
    def eval(self,n,env):
        if isinstance(n,Literal): return n.value
        if isinstance(n,Name):
            if n.value not in env: raise NameError(f"Undefined name: {n.value}")
            return env[n.value]
        if isinstance(n,Unary):
            v=self.eval(n.expr,env); return v if n.op=="+" else -v
        if isinstance(n,Binary):
            a,b=self.eval(n.left,env),self.eval(n.right,env)
            return {"+":lambda:a+b,"-":lambda:a-b,"*":lambda:a*b,"/":lambda:a/b,"%":lambda:a%b,
                    "==":lambda:a==b,"!=":lambda:a!=b,"<":lambda:a<b,"<=":lambda:a<=b,
                    ">":lambda:a>b,">=":lambda:a>=b}[n.op]()
        if isinstance(n,Call):
            f=self.eval(n.callee,env); args=[self.eval(x,env) for x in n.args]
            if not callable(f): raise TypeError("object is not callable")
            return f(args) if isinstance(f,FunctionValue) else f(*args)
        raise TypeError(type(n).__name__)

def run(source):
    p=parse(source); i=Interpreter(); i.exec_program(p); return i.env
