from lexer.lexer import Lexer
from lexer.lexer import TokenType

def test_lexer():
    lex = Lexer('string x = "Hejsa";')

    lex.lexer()

    assert lex.tokens[0].type == TokenType.TYPE
    assert lex.tokens[1].type == TokenType.IDENTIFIER
    assert lex.tokens[1].value == "x"
    assert lex.tokens[2].type == TokenType.ASSIGN
    assert lex.tokens[3].type == TokenType.STRING
    assert lex.tokens[3].value == "Hejsa"
    assert lex.tokens[4].type == TokenType.SEMICOLON
    assert lex.tokens[5].type == TokenType.EOF
    #and some more assertions 

def test_lexer():
    lex = Lexer('string x = "Hejsa";')

    lex.lexer()

    assert lex.tokens[0].type == TokenType.TYPE
    assert lex.tokens[1].type == TokenType.IDENTIFIER
    assert lex.tokens[1].value == "x"
    assert lex.tokens[2].type == TokenType.ASSIGN
    assert lex.tokens[3].type == TokenType.STRING
    assert lex.tokens[3].value == "Hejsa"
    assert lex.tokens[4].type == TokenType.SEMICOLON
    assert lex.tokens[5].type == TokenType.EOF
    #and some more assertions 