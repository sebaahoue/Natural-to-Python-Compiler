import ply.yacc as yacc

from lex import tokens
import AST

vars = {}

def p_programme_statement(p):
    ''' programme : statement '.' '''
    p[0] = AST.ProgramNode(p[1])

def p_programme_recursive(p):
    ''' programme : statement '.' programme '''
    p[0] = AST.ProgramNode([p[1]]+p[3].children)


def p_statement(p):
    ''' statement : assignation
        | structure '''
    p[0] = p[1]

def p_statement_print(p):
    ''' statement : AFFICHER expression'''
    p[0] = AST.PrintNode(p[2])

def p_structure_for(p):
    ''' structure : POUR iterateur TO loop DEBUT programme FIN'''
    p[0] = AST.ForNode([p[2],p[4],p[6]])

def p_iterateur(p):
    ''' iterateur : IDENTIFIER '''
    p[0] = AST.TokenNode(p[1])

def p_loop(p):
    ''' loop : range STEP expression '''
    p[0] = AST.LoopNode([p[1],p[3]])

def p_range(p):
    ''' range : expression A expression '''
    p[0] = AST.RangeNode([p[1],p[3]])

def p_structure_if(p):
    ''' structure : SI boolean DEBUT programme SINON programme FIN '''
    p[0]=AST.IfNode([p[2],p[4],p[6]])

def p_boolean(p):
    ''' boolean : expression COMPARABLE expression '''
    p[0]=AST.BoolNode(p[2],[p[1],p[3]])

def p_expression_num_or_var(p):
    '''expression : NUMBER
        | IDENTIFIER
        | STRING '''
    p[0] = AST.TokenNode(p[1])

def p_expression_op(p):
    '''expression : expression ADD_OP expression
            | expression MUL_OP expression'''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])

def p_assign(p):
    ''' assignation : IDENTIFIER VAUT expression '''
    p[0] = AST.AssignNode([AST.TokenNode(p[1]),p[3]])

def p_error(p):
    if p:
        print ("Syntax error in line %d" % p.lineno)
        yacc.errok()
    else:
        print ("Syntax error: unexpected end of file!")

precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
)

def parse(program):
    return yacc.parse(program)

yacc.yacc(outputdir='generated')


if __name__ == "__main__":
    import sys 
    	
    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog)
    if result:
        print (result)
            
        import os
        os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
        graph = result.makegraphicaltree()
        name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
        graph.write_pdf(name) 
        print ("wrote ast to", name)
    else:
        print ("Parsing returned no result!")