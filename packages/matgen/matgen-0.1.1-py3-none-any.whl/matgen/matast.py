from enum import Enum
from typing import List, Dict
import numpy as np

class TokenType(Enum):
    LEFT_B = '['
    RIGHT_B = ']'
    LEFT_P = '('
    RIGHT_P = ')'
    COLON = ';'
    COMMA = ','
    DIGIT = 'DIGIT'
    EXPR = 'EXPR'
    EOF = 'EOF'

class Token(object):
    def __init__(self, tokentype:TokenType, value:str, lineno:int, colno:int):
        self.tokentype:TokenType = tokentype
        self.value:str = value
        self.lineno:int = lineno
        self.colno:int = colno

    def __str__(self):
        return f'Token({self.tokentype}, {self.value}, position={self.lineno}:{self.colno})'

    def __repr__(self):
        return self.__str__()

class Lexer(object):
    def __init__(self, text:str):
        self.text:str = text
        self.pos:int = 0
        self.current_char:str = self.text[self.pos]
        self.lineno:int = 1
        self.colno:int = 1

    def pos_info(self) -> str:
        return f'{self.current_char} ({self.lineno}, {self.colno})'
    
    def error(self):
        raise ValueError(f'unexpected char at {self.pos_info()}')

    def advance(self):
        if self.current_char == '\n':
            self.lineno += 1
            self.colno = 0
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = ''  # Indicates the end of input
        else:
            self.current_char = self.text[self.pos]
            self.colno += 1

    def skip_whitespace(self):
        while self.current_char.isspace():
            self.advance()

    def parenthesis_advance(self):
        if self.current_char == '(':
            self.advance()
            while self.current_char != ')':
                self.parenthesis_advance()
        else:
            self.advance()
        
    def expr(self):
        start_pos = self.pos
        while (not self.current_char.isspace() and 
            self.current_char not in [',', '[', ']', ';']):
            self.parenthesis_advance()
        if self.pos < start_pos:
            raise ValueError(f'not a expr at {self.pos_info()}')
        return eval(self.text[start_pos:self.pos])
    
    def digit(self):
        start_pos = self.pos
        while self.current_char.isdigit():
            self.advance()
        if self.current_char=='.':
            self.advance()
            while self.current_char.isdigit():
                self.advance()
            return float(self.text[start_pos:self.pos])
        else:
            return int(self.text[start_pos:self.pos])

    def get_next_token(self) -> Token:
        while self.current_char.isspace():
            self.skip_whitespace()
        if self.current_char.isdigit():
            return Token(TokenType.DIGIT, self.digit(), self.lineno, self.colno)
        elif self.current_char in [',', ';', '[', ']']:
            tokentype = TokenType(self.current_char)
            token = Token(
                tokentype=tokentype,
                value=tokentype.value,  # e.g. ';', '.', etc
                lineno=self.lineno,
                colno=self.colno,
            )
            self.advance()
            return token
        elif not self.current_char:
            return Token(TokenType.EOF, None, self.lineno, self.colno)
        else:
            return Token(TokenType.EXPR, self.expr(), self.lineno, self.colno)

class AST(object):
    pass

class DigitAST(AST):
    def __init__(self, digit_token:Token):
        self.digit_token:Token = digit_token

    def interpret(self) -> float:
        return self.digit_token.value

class ExprAST(AST):
    def __init__(self, expr_token:Token):
        self.expr_token:Token = expr_token

    def interpret(self) -> float:
        return self.expr_token.value

class RowAST(AST):
    def __init__(self):
        self.items_ast:List[AST] = []

    def interpret(self) -> np.ndarray:
        items = [item_ast.interpret() for item_ast in self.items_ast]
        return np.hstack(items)

class MatrixAST(AST):
    def __init__(self):
        self.rows_ast:List[RowAST] = []

    def interpret(self) -> np.ndarray:
        rows = [row_ast.interpret() for row_ast in self.rows_ast]
        return np.vstack(rows)
        
class Parser(object):
    def __init__(self, text:str):
        self.lexer:Lexer = Lexer(text)
        self.current_token:Token = self.lexer.get_next_token()

    def error(self):
        raise ValueError(f'Invalid syntax at {self.current_token}')

    def eat(self, tokentype:TokenType) -> Token:
        if self.current_token.tokentype == tokentype:
            previous_token = self.current_token
            self.current_token = self.lexer.get_next_token()
            return previous_token
        else:
            self.error()

    def row(self) -> RowAST:
        root:RowAST = RowAST()
        while self.current_token.tokentype not in (TokenType.RIGHT_B,
            TokenType.COLON):
            if self.current_token.tokentype == TokenType.DIGIT:
                root.items_ast.append(DigitAST(self.eat(TokenType.DIGIT)))
            elif self.current_token.tokentype == TokenType.LEFT_B:
                root.items_ast.append(self.matrix())
            elif self.current_token.tokentype == TokenType.EXPR:
                root.items_ast.append(ExprAST(self.eat(TokenType.EXPR)))
            else:
                self.error()
            if self.current_token.tokentype == TokenType.COMMA:
                self.eat(TokenType.COMMA)
        return root

    def matrix(self) -> MatrixAST:
        self.eat(TokenType.LEFT_B)
        root:MatrixAST = MatrixAST()
        while self.current_token.tokentype != TokenType.RIGHT_B:
            root.rows_ast.append(self.row())
            if self.current_token.tokentype == TokenType.COLON:
                self.eat(TokenType.COLON)
        self.eat(TokenType.RIGHT_B)
        return root

class Interpreter(object):
    def __init__(self, text):
        self.parser:Parser = Parser(text)

    def interpret(self) -> np.ndarray:
        matrix_ast:MatrixAST = self.parser.matrix()
        return matrix_ast.interpret()
