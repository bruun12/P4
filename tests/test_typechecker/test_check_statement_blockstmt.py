from type_checker.TypeChecker import IfStatement, TypeChecker, BlockStatement, TypeEnvironment, ExpressionStatement, Literal

#Collects all call used for the check_statement to campare with expected values
class SpyChecker(TypeChecker):
    def __init__(self):
        self.call=[]
        
    def check_statement(self, stmt, env, within_function):
        self.call.append((stmt, env, within_function)) #Saves the calls happening inside the check_statement
        super().check_statement(stmt, env, within_function) #Forwards the information to the real check_statement


#Test amount of staatement in block statement using within_function
def test_within_function_in_block_stmt():
    checker = SpyChecker()
    exp_stmt = ExpressionStatement(Literal(1, 2, 3), 1, 2) #Random line and column numbers
    exp_stmt2 = ExpressionStatement(Literal(2, 3, 4), 2, 2)

    block = BlockStatement([exp_stmt, exp_stmt2], 4,5)
    env = TypeEnvironment()
    
    checker.check_statement(block, env, within_function=True)
    
    flags = [call[2] for call in checker.call]
    
    outer_flag = flags[0]
    inner_flag = flags[1:]
    
    assert outer_flag == True
    assert inner_flag == [False, True]
    
#Test amount of staatement in block statement using within_function
def test_within_function_in_block_stmt_type_environment():
    checker = SpyChecker()
    exp_stmt = ExpressionStatement(Literal(1, 2, 3), 1, 2) #Random line and column numbers
    exp_stmt2 = ExpressionStatement(Literal(2, 3, 4), 2, 2)
           
    block = BlockStatement([exp_stmt, exp_stmt2], 4,5)
    env = TypeEnvironment()
    
    checker.check_statement(block, env, within_function=True)
    
    inner_environment = [call[1] for call in checker.call[1:]] #First env is the block statement
    
    for inner_environment in inner_environment:
        assert inner_environment is not env
        assert inner_environment.parent is env

#Test order of statements in black statament
def test_within_function_in_block_stmt_stmt_order():
    checker = SpyChecker()
    exp_stmt = ExpressionStatement(Literal(1, 2, 3), 1, 2) #Random line and column numbers
    exp_stmt2 = ExpressionStatement(Literal(2, 3, 4), 2, 2)
           
    block = BlockStatement([exp_stmt, exp_stmt2], 4,5)
    env = TypeEnvironment()
    
    checker.check_statement(block, env, within_function=True)
    stmts_seen = [call[0] for call in checker.call[1:]]
    assert stmts_seen == [exp_stmt, exp_stmt2]
    
#Test to ensure inner_within_function returns false when within_function is false    
def test_within_function_false_making_inner_within_function_false():
    checker = SpyChecker()
    exp_stmt = ExpressionStatement(Literal(1, 2, 3), 1, 2) #Random line and column numbers
    exp_stmt2 = ExpressionStatement(Literal(2, 3, 4), 2, 2)
           
    block = BlockStatement([exp_stmt, exp_stmt2], 4,5)
    env = TypeEnvironment()
    
    checker.check_statement(block, env, within_function=False)
    
    inner_flag = [call[2] for call in checker.call[1:]]
    assert inner_flag == [False, False] #Returns false eventhough the is_last_statment is true
    
    
#Test for nested block statements is in different environments/scopes
def test_nested_block_stmt():
    checker = SpyChecker()
    exp_stmt = ExpressionStatement(Literal(1, 2, 3), 1, 2) #Random line and column numbers
    exp_stmt2 = ExpressionStatement(Literal(2, 3, 4), 2, 2)
    
    if_block = IfStatement(Literal(True, 2, 3), exp_stmt, None, 6, 8) 
    
    block = BlockStatement([exp_stmt2, if_block], 4, 5) 
    env = TypeEnvironment()
        
    checker.check_statement(block, env, within_function=True)
    
    calls = checker.call
    
    #envs created. First [] = which call (stmt, env, flag/bool), second [] = which field in the call ([1] = env)
    outer_env = calls[0][1]
    block_env = calls[1][1]
    if_env = calls[3][1]
    
    exp_stmt2_scope =  calls[2][1]
    
    # block_stmt is in the outer env and therefore create a new
    assert block_env is not outer_env
    assert block_env.parent is outer_env
    
    assert exp_stmt2_scope is block_env
    
    # if_stmt is in the block_env and also create a new if_env (containing the then_branch)
    assert if_env is not block_env
    assert if_env.parent is block_env
    
#Check that the outmost blocktament is has None as the environment
def test_block_stmt_parent_is_None():
    checker = SpyChecker()
    exp_stmt = ExpressionStatement(Literal(1, 2, 3), 1, 2) #Random line and column numbers
    exp_stmt2 = ExpressionStatement(Literal(4, 2, 3), 1, 2)
        
    block = BlockStatement([exp_stmt, exp_stmt2], 4, 5)  
    env = TypeEnvironment()
        
    checker.check_statement(block, env, within_function=True)
    
    calls = checker.call
    
    #envs created. First [] = which call (stmt, env, flag/bool), second [] = which field in the call ([1] = env)
    outer_env = calls[0][1]
    
    # block_stmt is in the outer env and therefore create a new
    assert outer_env.parent is None
 
#Test empty blocks creates envs but is allowed   
def test_block_stmt_empty():
    checker = SpyChecker()
         
    block2 = BlockStatement([], 3, 6)
    block3 = BlockStatement([], 3, 6)
    outer_block = BlockStatement([block2, block3], 4, 5)  
    env = TypeEnvironment()
        
    checker.check_statement(outer_block, env, within_function=True)
    
    calls = checker.call
    
    #envs created. First [] = which call (stmt, env, flag/bool), second [] = which field in the call ([1] = env)
    outer_env = calls[0][1]
    block2_env = calls[1][1]
    block3_env = calls[2][1]    
    assert outer_env.parent is None    
    
    # block_stmt is in the outer env and therefore create a new
    assert block2_env.parent is outer_env
    assert block2_env is not outer_env
    
    assert block3_env.parent is outer_env
    assert block3_env is not outer_env