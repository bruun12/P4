from lexer.lexer import Lexer
from lexer.lexer import TokenType

def test_lexer_string_declaration():
    lex = Lexer('string x = "Hejsa";')

    lex.lexer()

    assert lex.tokens[0].type == TokenType.TYPE
    assert lex.tokens[0].value == "string"
    assert lex.tokens[1].type == TokenType.IDENTIFIER
    assert lex.tokens[1].value == "x"
    assert lex.tokens[2].type == TokenType.ASSIGN
    assert lex.tokens[3].type == TokenType.STRING
    assert lex.tokens[3].value == "Hejsa"
    assert lex.tokens[4].type == TokenType.SEMICOLON
    assert lex.tokens[5].type == TokenType.EOF
    #and some more assertions 


def test_lexer_integer_assignment():
    lex = Lexer("""
                integer i = 1;
                i = 455;
                """)

    lex.lexer()

    assert lex.tokens[0].type == TokenType.TYPE
    assert lex.tokens[0].value == "integer"
    assert lex.tokens[1].type == TokenType.IDENTIFIER
    assert lex.tokens[1].value == "i"
    assert lex.tokens[2].type == TokenType.ASSIGN
    assert lex.tokens[3].type == TokenType.INTEGER
    assert lex.tokens[3].value == 1
    assert lex.tokens[4].type == TokenType.SEMICOLON
    assert lex.tokens[5].type == TokenType.IDENTIFIER
    assert lex.tokens[5].value == "i"
    assert lex.tokens[6].type == TokenType.ASSIGN
    assert lex.tokens[7].type == TokenType.INTEGER
    assert lex.tokens[7].value == 455
    assert lex.tokens[8].type == TokenType.SEMICOLON
    assert lex.tokens[9].type == TokenType.EOF




def test_lexer_if_statement():
    lex = Lexer("""
                boolean b = True;
                if (b) {
                    b = False;
                } else {
                    b = True;
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
    assert lex.tokens[9].type == TokenType.LBRACE

    # b = False;
    assert lex.tokens[10].type == TokenType.IDENTIFIER
    assert lex.tokens[10].value == "b"
    assert lex.tokens[11].type == TokenType.ASSIGN
    assert lex.tokens[12].type == TokenType.FALSE
    assert lex.tokens[12].value == "false"
    assert lex.tokens[13].type == TokenType.SEMICOLON

    # } else {
    assert lex.tokens[14].type == TokenType.RBRACE
    assert lex.tokens[15].type == TokenType.ELSE
    assert lex.tokens[16].type == TokenType.LBRACE
    
    # b = True;
    assert lex.tokens[17].type == TokenType.IDENTIFIER
    assert lex.tokens[17].value == "b"
    assert lex.tokens[18].type == TokenType.ASSIGN
    assert lex.tokens[19].type == TokenType.TRUE
    assert lex.tokens[19].value == "true"
    assert lex.tokens[20].type == TokenType.SEMICOLON

    # }
    assert lex.tokens[21].type == TokenType.RBRACE
    assert lex.tokens[22].type == TokenType.EOF


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

"""

def test_lexer_while_statement():
    lex = Lexer("" "
                integer i = 0;
                float f = 2.0; 
                while (i < 5){
                    f = f * 2;
                    i = i + 1;
                }
                "" ")

    lex.lexer()

"""
