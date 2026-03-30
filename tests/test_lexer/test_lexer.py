from lexer.lexer import Lexer
from lexer.lexer import TokenType

def test_lexer_string_declaration():
    lex = Lexer('string x = "Hejsa";')

    lex.lexer()

    expected = [
        (TokenType.TYPE, "string"),
        (TokenType.IDENTIFIER, "x"),
        (TokenType.ASSIGN, "="),
        (TokenType.STRING, "Hejsa"),
        (TokenType.SEMICOLON, ";"),
        (TokenType.EOF, "EOF")
    ]
    
    actual = [(t.type, t.value) for t in lex.tokens]
    assert actual == expected


def test_lexer_integer_assignment():
    lex = Lexer("""
                integer i = 1;
                i = 455;
                """)

    lex.lexer()

    expected = [
        (TokenType.TYPE, "integer"),
        (TokenType.IDENTIFIER, "i"),
        (TokenType.ASSIGN, "="),
        (TokenType.INTEGER, 1),
        (TokenType.SEMICOLON, ";"),
        (TokenType.IDENTIFIER, "i"),
        (TokenType.ASSIGN, "="),
        (TokenType.INTEGER, 455),
        (TokenType.SEMICOLON, ";"),
        (TokenType.EOF, "EOF")
    ]
    
    actual = [(t.type, t.value) for t in lex.tokens]
    assert actual == expected



"""
def test_lexer_if_statement():
    lex = Lexer("" "
                boolean b = True;

                if (b) {
                    b = False;
                } else {
                    b = True;
                }
                "" ")

    lex.lexer()

"""


def test_lexer_while_statement():
    lex = Lexer("""
                integer i = 0;
                double f = 2.0; 
                while (i < 5){
                    f = f * 2;
                    i = i + 1;
                }       
                """)
    
    lex.lexer()
    
    expected = [
        (TokenType.TYPE, "integer"),
        (TokenType.IDENTIFIER, "i"),
        (TokenType.ASSIGN, "="),
        (TokenType.INTEGER, 0),
        (TokenType.SEMICOLON, ";"),
        (TokenType.TYPE, "double"),
        (TokenType.IDENTIFIER, "f"),
        (TokenType.ASSIGN, "="),
        (TokenType.FLOAT, 2.0),
        (TokenType.SEMICOLON, ";"),
        (TokenType.WHILE, "while"),
        (TokenType.LPAREN, "("),
        (TokenType.IDENTIFIER, "i"),
        (TokenType.LT, "<"),
        (TokenType.INTEGER, 5),
        (TokenType.RPAREN, ")"),
        (TokenType.LBRACE, "{"),
        (TokenType.IDENTIFIER, "f"),
        (TokenType.ASSIGN, "="),
        (TokenType.IDENTIFIER, "f"),
        (TokenType.STAR, "*"),
        (TokenType.INTEGER, 2),
        (TokenType.SEMICOLON, ";"),
        (TokenType.IDENTIFIER, "i"),
        (TokenType.ASSIGN, "="),
        (TokenType.IDENTIFIER, "i"),
        (TokenType.PLUS, "+"),
        (TokenType.INTEGER, 1),
        (TokenType.SEMICOLON, ";"),
        (TokenType.RBRACE, "}"),
        (TokenType.EOF, "EOF")
    ]
    
    actual = [(t.type, t.value) for t in lex.tokens]
    assert actual == expected

"""
    This is inspiration on how to test the lexer

    assert lex.tokens[0].type == TokenType.TYPE
    assert lex.tokens[1].type == TokenType.IDENTIFIER
    assert lex.tokens[1].value == "x"
    assert lex.tokens[2].type == TokenType.ASSIGN
    assert lex.tokens[3].type == TokenType.STRING
    assert lex.tokens[3].value == "Hejsa"
    assert lex.tokens[4].type == TokenType.SEMICOLON
    assert lex.tokens[5].type == TokenType.EOF
    #and some more assertions 
"""