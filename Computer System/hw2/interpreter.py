#типи токенів
class tokentype:
    integer, plus, minus, mul, div, lparen, rparen, eof = ('integer', 'plus', 'minus', 'mul', 'div', 'lparen', 'rparen', 'eof')

class token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

#лексер
class lexer:
    def __init__(self, text):
        self.text = text
        self.index = 0
        self.current_char = text[0] if text else None

    def advance(self):
        self.index += 1
        self.current_char = self.text[self.index] if self.index < len(self.text) else None

    def get_number(self):
        number = ''
        while self.current_char and self.current_char.isdigit():
            number += self.current_char
            self.advance()
        return int(number)

    def get_next_token(self):
        while self.current_char:
            if self.current_char.isspace():
                self.advance()
                continue
            if self.current_char.isdigit():
                return token(tokentype.integer, self.get_number())
            if self.current_char == '+':
                self.advance()
                return token(tokentype.plus, '+')
            if self.current_char == '-':
                self.advance()
                return token(tokentype.minus, '-')
            if self.current_char == '*':
                self.advance()
                return token(tokentype.mul, '*')
            if self.current_char == '/':
                self.advance()
                return token(tokentype.div, '/')
            if self.current_char == '(':
                self.advance()
                return token(tokentype.lparen, '(')
            if self.current_char == ')':
                self.advance()
                return token(tokentype.rparen, ')')
        return token(tokentype.eof, None)

class num:
    def __init__(self, value):
        self.value = value

class binop:
    def __init__(self, left, operation, right):
        self.left = left
        self.operation = operation
        self.right = right

#парсер
class parser:
    def __init__(self, lexer_obj):
        self.lexer = lexer_obj
        self.current_token = lexer_obj.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()

    #число або дужки
    def factor(self):
        current = self.current_token
        if current.type == tokentype.integer:
            self.eat(tokentype.integer)
            return num(current.value)
        self.eat(tokentype.lparen)
        node = self.expr()
        self.eat(tokentype.rparen)
        return node

    #множення і ділення
    def term(self):
        node = self.factor()
        while self.current_token.type in (tokentype.mul, tokentype.div):
            operation = self.current_token
            if operation.type == tokentype.mul:
                self.eat(tokentype.mul)
            else:
                self.eat(tokentype.div)
            node = binop(node, operation, self.factor())
        return node

    #додавання і віднімання
    def expr(self):
        node = self.term()

        while self.current_token.type in (tokentype.plus, tokentype.minus):
            operation = self.current_token
            if operation.type == tokentype.plus:
                self.eat(tokentype.plus)
            else:
                self.eat(tokentype.minus)
            node = binop(node, operation, self.term())
        return node

#інтерпретатор
class interpreter:
    def __init__(self, parser_obj):
        self.parser = parser_obj

    def visit(self, node):
        if isinstance(node, num):
            return node.value
        if node.operation.type == tokentype.plus:
            return self.visit(node.left) + self.visit(node.right)
        if node.operation.type == tokentype.minus:
            return self.visit(node.left) - self.visit(node.right)
        if node.operation.type == tokentype.mul:
            return self.visit(node.left) * self.visit(node.right)
        if node.operation.type == tokentype.div:
            return self.visit(node.left) // self.visit(node.right)

    def run(self):
        return self.visit(self.parser.expr())

#тест
expression = "(2+3) * 4"
lexer_obj = lexer(expression)
parser_obj = parser(lexer_obj)
interpreter_obj = interpreter(parser_obj)
result = interpreter_obj.run()
print(result)