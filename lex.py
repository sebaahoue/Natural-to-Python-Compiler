'''
Module contenant l'analyseur lexical du langage Natural.
Il inclus la spécification de la grammaire, les conventions de nommage
ainsi que les mots reserves du langage.
'''

import ply.lex as lex

# mots reserves du langage
reserved_words = (
    'a',
    'vaut',
    'pour',
    'afficher',
    'si',
    'sinon',
    'debut',
    'fin'
)

# extension des mots reserves avec d'autres mots interdits
extended_reserved_words = (
    'plus',
    'moins',
    'divise',
    'par',
    'fois',
    'allant',
    'de',
    'pas',
    'inferieur',
    'superieur',
) + reserved_words

# definition des lexemes
tokens = (
    'NUMBER',
    'ADD_OP',
    'MUL_OP',
    'COMPARABLE',
    'TO',
    'STEP',
    'IDENTIFIER',
    'STRING'
) + tuple(map(lambda s:s.upper(),reserved_words))

literals = '.,'

'''
Description des différents lexèmes
'''
# operateur d'addition
def t_ADD_OP(t):
	r'plus|moins'
	return t

# operateur de multiplication
def t_MUL_OP(t):
    r'fois|divise[ ]par'
    return t

# comparaison
def t_COMPARABLE(t):
    r'inferieur[ ]a|superieur[ ]a|egal[ ]a'
    return t

# range (boucle for)
def t_TO(t):
    r'allant[ ]de'
    return t

# pas (boucle for)
def t_STEP(t):
    r'par[ ]pas[ ]de'
    return t

# nombre
def t_NUMBER(t):
    r'\d+([,]\d+)?'
    t.value = t.value.replace(',','.')
    try:
        if '.' in t.value:
            t.value = float(t.value)
        else:
            t.value = int(t.value)

    except ValueError:
        print ("Line %d: Problem while parsing %s!" % (t.lineno,t.value))
        t.value = 0
    return t

# string
def t_STRING(t):
    r'\'(.*?)\''
    t.value = t.value.replace('\'','')
    return t

def t_IDENTIFIER(t):
    r'[A-Za-z_]\w*'
    if t.value in reserved_words:
        t.type = t.value.upper()
    return t

# délimiteur de nouvelle ligne
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

# erreurs
def t_error(t):
	print ("Illegal character '%s'" % repr(t.value[0]))
	t.lexer.skip(1)

lex.lex()

if __name__ == "__main__":
	import sys
	prog = open(sys.argv[1]).read()

	lex.input(prog)

	while 1:
		tok = lex.token()
		if not tok: break
		print ("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))