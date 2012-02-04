from ply.lex import TOKEN
import ply.lex as lex
import re

reserved = {
    'and'     : 'AND',
    'break'   : 'BREAK',
    'class'   : 'CLASS',
    'continue': 'CONTINUE',
    'def'     : 'DEF',
    'elif'    : 'ELIF',
    'else'    : 'ELSE',
    'for'     : 'FOR',
    'if'      : 'IF',
    'in'      : 'IN',
    'is'      : 'IS',
    'not'     : 'NOT',
    'or'      : 'OR',
    'pass'    : 'PASS',
    'print'   : 'PRINT',
    'return'  : 'RETURN',
    'while'   : 'WHILE',
}

tokens = ['PLUS',
          'MINUS',
          'STAR',
          'SLASH',
          'DOUBLESLASH',
          'VBAR',
          'AMPER',
          'LESS',
          'GREATER',
          'PERCENT',
          'CIRCUMFLEX',
          'TILDE',
          'EQUAL',
          'NOTEQUAL',
          'ALT_NOTEQUAL',
          'LESSEQUAL',
          'GREATEREQUAL',
          'LEFTSHIFT',
          'RIGHTSHIFT',
          'DOUBLESTAR',
          'ASSIGN',
          'PLUSEQUAL',
          'MINUSEQUAL',
          'STAREQUAL',
          'SLASHEQUAL',
          'VBAREQUAL',
          'PERCENTEQUAL',
          'AMPEREQUAL',
          'CIRCUMFLEXEQUAL',
          'LEFTSHIFTEQUAL',
          'RIGHTSHIFTEQUAL',
          'DOUBLESTAREQUAL',
          'LPAREN',
          'RPAREN',
          'LBRACK',
          'RBRACK',
          'COMMA',
          'DOT',
          'SEMI',
          'COLON',
          'LONGINT',
          'INT',
          'FLOAT',
          'STRING',
          'NEWLINE',
          'INDENT',
          'DEDENT',
          'ID', ]\
           + list(reserved.values())

# Operators
t_PLUS = r'\+'
t_MINUS = r'-'
t_STAR = r'\*'
t_SLASH = r'/'
t_DOUBLESLASH = r'//'
t_VBAR = r'\|'
t_AMPER = r'&'
t_LESS = r'<'
t_GREATER = r'>'
t_PERCENT = r'%'
t_CIRCUMFLEX = r'\^'
t_TILDE = r'~'
t_EQUAL = r'=='
t_NOTEQUAL = r'!='
t_ALT_NOTEQUAL = r'<>'
t_LESSEQUAL = r'<='
t_GREATEREQUAL = r'>='
t_LEFTSHIFT = r'<<'
t_RIGHTSHIFT = r'>>'
t_DOUBLESTAR = r'\*\*'

# Assignment operators
t_ASSIGN = r'='
t_PLUSEQUAL = r'\+='
t_MINUSEQUAL = r'-='
t_STAREQUAL = r'\*='
t_SLASHEQUAL = r'/='
t_VBAREQUAL = r'\|='
t_PERCENTEQUAL = r'%='
t_AMPEREQUAL = r'&='
t_CIRCUMFLEXEQUAL = r'\^='
t_LEFTSHIFTEQUAL = r'<<='
t_RIGHTSHIFTEQUAL = r'>>='
t_DOUBLESTAREQUAL = r'\*\*='

# Delimiters
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_COMMA = r','
t_DOT = r'\.'
t_SEMI = r';'
t_COLON = r':'

#numbers
def t_FLOAT(t):
    r'\.\d+([eE](\+|-)?\d+)?|\d+\.\d*([eE](\+|-)?\d+)?|\d+[eE](\+|-)?\d+'
    t.value = float(t.value)
    return t

rInt = r'(0[xX][0-9a-fA-F]+|0[bB][01]+|0?\d+)'
rLong = rInt + r'[lL]'

@TOKEN(rLong)
def t_LONGINT(t):
    getIntValue(t, long)
    return t

@TOKEN(rInt)
def t_INT(t):
    getIntValue(t, int)
    return t

def getIntValue(t, f):
    if t.value.startswith('0x'):
        t.value = f(t.value, 16)
    elif t.value.startswith('0b'):
        t.value = f(t.value, 2)
    elif t.value.startswith('0'):
        t.value = f(t.value, 8)
    else:
        t.value = f(t.value)

# string
rString = r"'.*?'"

@TOKEN(rString)   
def t_STRING(t):
    t.value = eval(t.value)
    return t

# identifier
def t_NAME(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# newline or dedent
# use a stack to keep track of indent
def setIfDedent(t):
    lexer = t.lexer
    ws = re.match(r'[ \t]*', lexer.lexdata[lexer.lexpos:]).group()
    top = lexer.stack[-1]
    if lexer.isDedent:
        if ws not in lexer.stack: raise "Indentation Error!"
        t.type = 'DEDENT'
        lexer.isDedent = False
    if len(top) <= len(ws):
        lexer.lexpos += len(top)
        lexer.newline = True
    else:
        lexer.stack.pop()
        lexer.lexpos -= 1
        lexer.isDedent = True

def t_NEWLINE(t):
    r'([ \t]*\r?\n)+'
    setIfDedent(t)
    return t

# indent
def t_INDENT(t):
    r'[ \t]+'
    t.lexer.stack.append(t.lexer.stack[-1] + t.value)
    return t

# ignore
t_ignore = ' \t'
t_ignore_COMMENT = r'\#[^\n]*'

def t_error(t):
    print 'Lexical Error'

lexer = lex.lex()
lexer.stack = ['']
lexer.isDedent = False
lexer.newline = True