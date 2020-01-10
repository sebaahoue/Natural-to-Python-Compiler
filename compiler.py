'''
Module contenant le compilateur du langage Natural vers Python.
Il a pour role de traduire le code source(Natural) en code output(python).
Pour cela, il parcours l'arbre syntaxique et traduit chacun des noeuds.
'''

import AST
from AST import addToClass

# définition des équivalents des opérations mathématiques
operations = {
	'plus' : '+',
	'moins' : '-',
	'fois' : '*',
	'divise' : '/'
}

# définition des équivalents des opérateurs de condition
conditions = {
	'superieur a' : '>',
	'inferieur a' : '<',
	'egal a' : '='
}

variable = dict()

def tabcounter():
	tabcounter.current += 1
	return tabcounter.current
tabcounter.current = 0

# compile chacun des noeuds enfants d'un programme
@addToClass(AST.ProgramNode)
def compile(self):
	bytecode = ""
	for c in self.children:
		bytecode += c.compile()
	return bytecode

# compile les tokens
@addToClass(AST.TokenNode)
def compile(self):
    bytecode = ""
    if not (self.tok in variable.keys() or isinstance(self.tok,(int,float))):
        print("'%s' variable must be instantiate before utilisation" % self.tok)
    bytecode += "%s" % self.tok
    return bytecode

# compile les noeuds d'assignation
@addToClass(AST.AssignNode)
def compile(self):
    bytecode = ""
    bytecode += "%s = " % self.children[0].tok
    bytecode += "%s \n" % self.children[1].compile()
    variable[self.children[0].tok] = self.children[1].compile()
    return bytecode

# compile les noeuds d'affichage
@addToClass(AST.PrintNode)
def compile(self):
    bytecode = ""
    content = self.children[0].compile()
    bytecode += "print(%s)\n" % content
    return bytecode

# compile les noeuds de chaines de caracteres
@addToClass(AST.TokenStringNode)
def compile(self):
    bytecode = ""
    bytecode += "'%s'" % self.tok
    return bytecode

# compile les noeuds d'opérateurs
@addToClass(AST.OpNode)
def compile(self):
    bytecode = ""
    bytecode += self.children[0].compile()
    bytecode += " %s " % operations[self.op]
    bytecode += self.children[1].compile() + "\n"
    return bytecode

# compile les noeuds des boucles for
@addToClass(AST.ForNode)
def compile(self):
    counter = tabcounter()
    bytecode =""
    bytecode += "for %s in %s:\n" % (self.children[0].compile(),self.children[1].compile())
    for child in self.children[2].children:
        for i in range(counter):
            bytecode += "\t"
        bytecode += "%s" % child.compile()
    tabcounter.current = 0

    return bytecode

# compile les noeuds internes aux boucles
@addToClass(AST.LoopNode)
def compile(self):
    bytecode =""
    bytecode += "%s,%s)" % (self.children[0].compile(),self.children[1].compile())
    return bytecode

# compile les noeuds de type range
@addToClass(AST.RangeNode)
def compile(self):
    bytecode =""
    bytecode += "range(%s,%s" % (self.children[0].compile(),self.children[1].compile())
    return bytecode

# compile les noeuds de type if
@addToClass(AST.IfNode)
def compile(self):
    counter = tabcounter()
    tabs= ""
    for i in range(counter-1):
        tabs+="\t"
    bytecode =""
    bytecode += "if %s:\n" % self.children[0].compile()
    for child in self.children[1].children:
        bytecode += "%s\t%s" % (tabs,child.compile())
    bytecode += "%selse:\n" % tabs
    for child in self.children[2].children:
        bytecode += "%s\t%s" % (tabs,child.compile())
    tabcounter.current=0
    return bytecode

# compile les noeuds d'expressions booleenes
@addToClass(AST.BoolNode)
def compile(self):
    bytecode =""
    bytecode += "%s %s %s" % (self.children[0].compile(),conditions[self.cond],self.children[1].compile())
    return bytecode

if __name__ == "__main__":
    from naturalParser import parse
    import sys, os
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    print(ast)
    compiled = ast.compile()
    name = os.path.splitext(sys.argv[1])[0]+'.py'    
    outfile = open(name, 'w')
    outfile.write(compiled)
    outfile.close()
    print ("Wrote output to", name)