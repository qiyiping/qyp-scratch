from __future__ import print_function
from collections import namedtuple

Token = namedtuple('Token', ["type", "value"])

NUMBER, POINT, LPR, RPR, ADD, SUB, MUL, DIV, EOF = \
    "NUMBER", ".", "(", ")", "+", "-", "*", "/", "EOF"

OP_FUNC_DICT = {
    ADD: lambda x, y: x+y,
    SUB: lambda x, y: x-y,
    MUL: lambda x, y: x*y,
    DIV: lambda x, y: x/y
}

SPECS = [NUMBER, POINT, LPR, RPR, ADD, SUB, MUL, DIV, EOF]


# Text --> Tokens
class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else EOF

    def skip_whitespace(self):
        while self.current_char.isspace():
            self.advance()

    def error(self):
        raise Exception("Invalid Syntax")

    def number(self):
        buf = [self.current_char]
        self.advance()
        while self.current_char.isdigit() or self.current_char == ".":
            buf.append(self.current_char)
            self.advance()
        try:
            return float("".join(buf))
        except:
            self.error()

    def get_next_token(self):
        if self.current_char.isspace():
            self.skip_whitespace()
        if self.current_char in SPECS[2:]:
            token = Token(self.current_char, self.current_char)
            self.advance()
            return token
        if self.current_char.isdigit() or self.current_char == ".":
            return Token(NUMBER, self.number())
        self.error()


# Tokens --> AST
class Node(object):
    pass


class BinOpNode(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op.type
        self.right = right


class NumNode(Node):
    def __init__(self, token):
        self.value = token.value


class UnaryOpNode(Node):
    def __init__(self, token, expr):
        self.expr = expr
        self.op = token.type


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception("Invalid Syntax")

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def parse(self):
        ast = self.expr()
        self.eat(EOF)
        return ast

    # expr: term((+|-)term)*
    # term: factor((*|/)factor)*
    # factor: (+|-) factor | NUMBER | LPR expr RPR
    def expr(self):
        node = self.term()
        while self.current_token.type in (ADD, SUB):
            token = self.current_token
            self.eat(token.type)
            node = BinOpNode(node, token, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            self.eat(token.type)
            node = BinOpNode(node, token, self.factor())
        return node

    def factor(self):
        if self.current_token.type in (ADD, SUB):
            token = self.current_token
            self.eat(token.type)
            return UnaryOpNode(token, self.factor())
        if self.current_token.type == NUMBER:
            token = self.current_token
            self.eat(NUMBER)
            return NumNode(token)
        if self.current_token.type == LPR:
            self.eat(LPR)
            node = self.expr()
            self.eat(RPR)
            return node
        self.error()


# intepretor: ast --> value? ast --> machine code? ast --> assembly?
class Visitor(object):
    def visit(self, root):
        method_name = "visit_" + type(root).__name__
        visitor = getattr(self, method_name, self.default_visitor)
        return visitor(root)

    def default_visitor(self, root):
        raise Exception("Unsupported Visitor for Node type {}".format(type(root).__name__))


class Interpreter(Visitor):
    def __init__(self, ast):
        self.ast = ast

    def eval(self):
        return self.visit(self.ast)

    def error(self):
        raise Exception("Interpreter Error")

    def visit_BinOpNode(self, root):
        v_left = self.visit(root.left)
        v_right = self.visit(root.right)
        return OP_FUNC_DICT[root.op](v_left, v_right)

    def visit_NumNode(self, root):
        return root.value

    def visit_UnaryOpNode(self, root):
        expr = self.visit(root.expr)
        if root.op == SUB:
            return -expr
        elif root.op == ADD:
            return expr
        self.error()


class LispInterpreter(Visitor):
    def __init__(self, ast):
        self.ast = ast

    def eval(self):
        return self.visit(self.ast)

    def error(self):
        raise Exception("Interpreter Error")

    def visit_BinOpNode(self, root):
        v_left = self.visit(root.left)
        v_right = self.visit(root.right)
        return "({} {} {})".format(root.op, v_left, v_right)

    def visit_NumNode(self, root):
        return str(root.value)

    def visit_UnaryOpNode(self, root):
        expr = self.visit(root.expr)
        return "({} {})".format(root.op, expr)


# REPL
def main():
    import traceback
    while True:
        try:
            text = input("calc> ")
            if text in ("quit", "exit"):
                break
            lexer = Lexer(text)
            parser = Parser(lexer)
            ast = parser.parse()
            intepreter = Interpreter(ast)
            lisp_intepreter = LispInterpreter(ast)
            print(lisp_intepreter.eval())
            print(intepreter.eval())
        except Exception as exp:
            print(exp)
            traceback.print_exc()


if __name__ == '__main__':
    main()
