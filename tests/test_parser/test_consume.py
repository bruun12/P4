from parser.parser import Parser
from lexer.lexer import Lexer, TokenType, Token

def test_comsume():
    string = "integer x = 20 // initilizing x\ny = x * 5"
    lex = Lexer(string)

    lex.lexer()

    parser = Parser(lex.tokens)
    
    expected_current_token = Token(TokenType.TYPE, "integer", 0, 1)
    
    assert parser.consume(expected_current_token, "error message") == expected_current_token

    #while parser.current().type != TokenType.EOF:
    #    parser.advance()

    #assert parser.check(TokenType.EOF)
