from parser import *
from api.voice import speak, process_voice_command

class ReturnSignal(Exception):
    def __init__(self, value): self.value = value

class FunctionValue:
    def __init__(self, node, closure):
        self.node = node
        self.closure = closure

    def __call__(self, args):
        if len(args) != len(self.node.params):
            raise TypeError("wrong number of arguments")
        env = dict(self.closure)
        env.update(zip(self.node.params, args))
        try:
            Interpreter().exec_block(self.node.body, env)
        except ReturnSignal as signal:
            return signal.value
        return None

class Interpreter:
    def __init__(self):
        self.env = {}

    def exec_program(self, program):
        for statement in program.statements:
            self.exec_stmt(statement, self.env)

    def exec_block(self, block, env):
        for statement in block.statements:
            self.exec_stmt(statement, env)

    def exec_stmt(self, statement, env):
        if isinstance(statement, Set):
            env[statement.name] = self.eval(statement.expr, env)
        elif isinstance(statement, Show):
            print(self.eval(statement.expr, env))
        elif isinstance(statement, ExprStmt):
            self.eval(statement.expr, env)
        elif isinstance(statement, Block):
            self.exec_block(statement, env)
        elif isinstance(statement, Check):
            if self.eval(statement.condition, env):
                self.exec_block(statement.then, env)
            elif statement.otherwise:
                self.exec_block(statement.otherwise, env)
        elif isinstance(statement, Repeat):
            guard = 0
            while self.eval(statement.condition, env):
                guard += 1
                if guard > 1_000_000:
                    raise RuntimeError("repeat limit exceeded")
                self.exec_block(statement.body, env)
        elif isinstance(statement, Function):
            env[statement.name] = FunctionValue(statement, env)
        elif isinstance(statement, Give):
            raise ReturnSignal(None if statement.expr is None else self.eval(statement.expr, env))
        elif isinstance(statement, Finish):
            return

    def eval(self, node, env):
        if isinstance(node, Literal):
            return node.value
        if isinstance(node, Name):
            if node.value not in env:
                raise NameError(f"Undefined name: {node.value}")
            return env[node.value]
        if isinstance(node, Unary):
            value = self.eval(node.expr, env)
            return value if node.op == "+" else -value
        if isinstance(node, Binary):
            left = self.eval(node.left, env)
            right = self.eval(node.right, env)
            operations = {
                "+": lambda: left + right,
                "-": lambda: left - right,
                "*": lambda: left * right,
                "/": lambda: left / right,
                "%": lambda: left % right,
                "==": lambda: left == right,
                "!=": lambda: left != right,
                "<": lambda: left < right,
                "<=": lambda: left <= right,
                ">": lambda: left > right,
                ">=": lambda: left >= right,
            }
            return operations[node.op]()
        if isinstance(node, Call):
            function = self.eval(node.callee, env)
            args = [self.eval(argument, env) for argument in node.args]
            if not callable(function):
                raise TypeError("object is not callable")
            return function(args) if isinstance(function, FunctionValue) else function(*args)
        raise TypeError(type(node).__name__)


def run(source):
    program = parse(source)
    interpreter = Interpreter()
    interpreter.exec_program(program)
    return interpreter.env


def run_voice(command):
    command = process_voice_command(command)
    if not command:
        return None
    return run(command)
