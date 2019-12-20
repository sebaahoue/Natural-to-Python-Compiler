import AST
from AST import addToClass


operations = {
	'plus' : '+',
	'moins' : '-',
	'fois' : '*',
	'divise' : '/'
}

conditions = {
	'superieur a' : '>',
	'inferieur a' : '<',
	'egal a' : '='
}

def tabcounter():
	tabcounter.current += 1
	return tabcounter.current
tabcounter.current = 0

@addToClass(AST.ProgramNode)
def compile(self):
	bytecode = ""
	for c in self.children:
		bytecode += c.compile()
	return bytecode

@addToClass(AST.TokenNode)
def compile(self):
	bytecode = ""
	bytecode += "%s" % self.tok
	return bytecode

@addToClass(AST.AssignNode)
def compile(self):
    bytecode = ""
    bytecode += "%s = " % self.children[0].tok
    bytecode += "%s \n" % self.children[1].compile()
    return bytecode

@addToClass(AST.PrintNode)
def compile(self):
    bytecode = ""
    #définir le type du token STRING ou IDENTIFIER
    #if self.children[0].tok == "STRING":
    bytecode += "print(\'%s\')\n" % self.children[0].compile()
    #else:
    #    bytecode += "print(%s)\n" % self.children[0].tok
    return bytecode

@addToClass(AST.OpNode)
def compile(self):
    bytecode = ""
    bytecode += self.children[0].compile()
    bytecode += " %s " % operations[self.op]
    bytecode += self.children[1].compile() + "\n"
    return bytecode

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

@addToClass(AST.LoopNode)
def compile(self):
    bytecode =""
    bytecode += "%s,%s)" % (self.children[0].compile(),self.children[1].compile())
    return bytecode


@addToClass(AST.RangeNode)
def compile(self):
    bytecode =""
    bytecode += "range(%s,%s" % (self.children[0].compile(),self.children[1].compile())
    return bytecode


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