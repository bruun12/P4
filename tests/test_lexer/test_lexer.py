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




def test_lexer_if_statement():
    lex = Lexer("""
                boolean b = true;
                if (b) {
                    b = false;
                } else {
                    b = true;
                }
                """)
    lex.lexer()
    
    # boolean b = True;
    assert lex.tokens[0].type == TokenType.TYPE
    assert lex.tokens[0].value == "boolean"
    assert lex.tokens[1].type == TokenType.IDENTIFIER
    assert lex.tokens[1].value == "b"
    assert lex.tokens[2].type == TokenType.ASSIGN
    assert lex.tokens[3].type == TokenType.TRUE
    assert lex.tokens[3].value == "true"
    assert lex.tokens[4].type == TokenType.SEMICOLON

    # if (b) {
    assert lex.tokens[5].type == TokenType.IF
    assert lex.tokens[6].type == TokenType.LPAREN
    assert lex.tokens[7].type == TokenType.IDENTIFIER
    assert lex.tokens[7].value == "b"
    assert lex.tokens[8].type == TokenType.RPAREN
    assert lex.tokens[9].type == TokenType.LCBRACE

    # b = False;
    assert lex.tokens[10].type == TokenType.IDENTIFIER
    assert lex.tokens[10].value == "b"
    assert lex.tokens[11].type == TokenType.ASSIGN
    assert lex.tokens[12].type == TokenType.FALSE
    assert lex.tokens[12].value == "false"
    assert lex.tokens[13].type == TokenType.SEMICOLON

    # } else {
    assert lex.tokens[14].type == TokenType.RCBRACE
    assert lex.tokens[15].type == TokenType.ELSE
    assert lex.tokens[16].type == TokenType.LCBRACE
    
    # b = True;
    assert lex.tokens[17].type == TokenType.IDENTIFIER
    assert lex.tokens[17].value == "b"
    assert lex.tokens[18].type == TokenType.ASSIGN
    assert lex.tokens[19].type == TokenType.TRUE
    assert lex.tokens[19].value == "true"
    assert lex.tokens[20].type == TokenType.SEMICOLON

    # }
    assert lex.tokens[21].type == TokenType.RCBRACE
    assert lex.tokens[22].type == TokenType.EOF




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
        (TokenType.LCBRACE, "{"),
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
        (TokenType.RCBRACE, "}"),
        (TokenType.EOF, "EOF")
    ]
    
    actual = [(t.type, t.value) for t in lex.tokens]
    assert actual == expected
