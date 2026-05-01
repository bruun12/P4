from type_checker.TypeChecker import TypeChecker, BlockStatement, TypeEnvironment, Statement, NO_FLOW, RETURNS


class MockStmt(Statement):
    def __init__(self):
        super().__init__(line=0, column=0)
    
    ## Test Block Statement
def test_empty_block():
    env = TypeEnvironment(parent=None)
    stmt = BlockStatement(statements=[], line=0, column=0)
    checker = TypeChecker(source_code="")

    result = checker.check_statement(stmt, env)

    assert result == NO_FLOW
        
    
def test_block_not_returns():
    env = TypeEnvironment(parent=None)
    stmt = BlockStatement(statements=[MockStmt()], line=0, column=0)
    checker = TypeChecker(source_code="")

    oprindeligCheck = checker.check_statement

    def fake_check_statement(stmt, env):
        if isinstance(stmt, MockStmt):
            return NO_FLOW
        return oprindeligCheck(stmt, env)

    checker.check_statement = fake_check_statement 

    result = checker.check_statement(stmt, env)
                                             
    assert result == NO_FLOW
        

def test_block_returns():
    env = TypeEnvironment(parent=None)
    stmt = BlockStatement(statements=[MockStmt()], line=0, column=0)
    checker = TypeChecker(source_code="")

    oprindeligCheck = checker.check_statement

    def fake_check_statement(stmt, env):
        if isinstance(stmt, MockStmt):
            return RETURNS
        return oprindeligCheck(stmt, env)

    checker.check_statement = fake_check_statement 

    result = checker.check_statement(stmt, env)
                                             
    assert result == RETURNS
    

def test_more_stmts_last_block_returns():
    env = TypeEnvironment(parent=None)
    checker = TypeChecker(source_code="")

    stmt1 = MockStmt()
    stmt2 = MockStmt()
    stmt3 = MockStmt()

    stmt = BlockStatement(statements=[stmt1, stmt2, stmt3], line=0, column=0)

    call_count = 0

    oprindeligChecker = checker.check_statement

    def fake_check_stmt(stmt, env):
        nonlocal call_count

        if isinstance(stmt, MockStmt):
            call_count += 1
            if call_count < 3:
                return NO_FLOW
            else:
                return RETURNS
        return oprindeligChecker(stmt, env)
        
    checker.check_statement = fake_check_stmt

    result = checker.check_statement(stmt, env)

    assert result == RETURNS

    
def test_test_more_stmts_first_block_returns():
    env = TypeEnvironment(parent=None)
    checker = TypeChecker(source_code="")

    stmt1 = MockStmt()
    stmt2 = MockStmt()
    stmt3 = MockStmt()

    stmt = BlockStatement(statements=[stmt1, stmt2, stmt3], line=0, column=0)

    call_count = 0

    oprindeligChecker = checker.check_statement

    def fake_check_stmt(stmt, env):
        nonlocal call_count

            # det her er forkert - den skal starte med at kigge på den første, returner den, og så tage de to næste uden af returnerer
            # men den skal ikke køre mere end det fordi så looper den ik? 
        if isinstance(stmt, MockStmt):
            call_count += 1 
            if call_count > 0:
                return NO_FLOW
            else:
                return RETURNS
        return oprindeligChecker(stmt, env)
        
    checker.check_statement = fake_check_stmt

    result = checker.check_statement(stmt, env)

    assert result == RETURNS
    
''' 
    def test_unreacable_block_stmt(self):
'''
    
