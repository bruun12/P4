from lexer.lexer import Lexer
from lexer.token import TokenType
from lexer.token import KEYWORDS

# Checks if it correctly reads the specific identifiers or keywords and return a token type


# Checks it correctly handles values that is neither a keyword nor type
def test_read_word_identifier():
    lexer = Lexer('id')
    token = lexer.read_word()

    assert token.type == TokenType.IDENTIFIER
    assert token.value == "id"

# Checks it correctly handles keywords
def test_read_word_keyword_while():
    lexer = Lexer('while')
    token = lexer.read_word()

    assert token.type == TokenType.WHILE
    assert token.value == "while"

# Checks to ensure the types must have a precise TokenType
def test_read_word_keyword_while2():
    lexer = Lexer('while')
    token = lexer.read_word()

    assert not token.type == KEYWORDS
    assert token.value == "while"

# Checks it correctly handles types
def test_read_word_type_integer():
    lexer = Lexer('integer')
    token = lexer.read_word()

    assert token.type == TokenType.TYPE
    assert token.value == "integer"

# Checks it correctly handles types
def test_read_word_type_string():
    lexer = Lexer('string')
    token = lexer.read_word()

    assert token.type == TokenType.TYPE
    assert token.value == "string"

# Checks it correctly handles types
def test_read_word_type_double():
    lexer = Lexer('double')
    token = lexer.read_word()
    
    assert token.type == TokenType.TYPE
    assert token.value == "double"

# Checks it correctly reads underscore and will not skip it
def test_reads_underscore():
    lexer = Lexer("_____long____________identifier")
    token = lexer.read_word()

    assert token.type == TokenType.IDENTIFIER
    assert token.value == "_____long____________identifier"

# Checks it correctly reads an identifier surrounded by numbers
def test_reads_identifier_and_number():
    lexer = Lexer('1234567890identifier1234567890identifier')
    token = lexer.read_word()

    assert token.type == TokenType.IDENTIFIER
    assert token.value == "1234567890identifier1234567890identifier"

# Checks it correctly handles a dash
def test_reads_no_dash():
    lexer = Lexer('no-dash-')
    token = lexer.read_word()

    assert token.type == TokenType.IDENTIFIER
    assert not token.value == "no-dash-"
    assert token.value == "no"

# Checks it correctly handles empty strings
def test_reads_empty_string():
    lexer = Lexer("")
    token = lexer.read_word()

    assert token.type == TokenType.IDENTIFIER
    assert token.value == ""

# Checks it stops reading the word when hitting other values than keywords/types/identifiers
def test_reads_not_words():
    lexer = Lexer("hello;")
    token = lexer.read_word()

    assert token.type == TokenType.IDENTIFIER
    assert token.value == "hello"
    assert lexer.current_char() == ";"