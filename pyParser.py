import ply.yacc as yacc
from lexer import tokens
from ast import *

precedence = (
             ('right', 'PRINT'),
             ('left', 'VBAR', 'AMPER', 'CIRCUMFLEX'),
             ('left', 'LESS', 'GREATER', 'LESSEQUAL', 'GREATEREQUAL', 'EQUAL', 'NOTEQUAL', 'ALT_NOTEQUAL', 'IN', 'NOT', 'IS'),
             ('left', 'PLUS', 'MINUS'),
             ('left', 'STAR', 'SLASH', 'PERCENT'),
             ('left', 'LEFTSHIFT', 'RIGHTSHIFT', 'DOUBLESTAR', 'TILDE'),
             ('nonassoc', 'LPAREN', 'RPAREN')
)

def p_input(p):
    '''input : help_star'''
    p[0] = Module(None, Stmt(p[1]))
    
def p_help_star_1(p):
    '''help_star : help_star stmt'''
    p[0] = p[1] + p[2]    
    
def p_help_star_2(p):
    '''help_star : help_star NEWLINE'''
    p[0] = p[1]
    
def p_help_star_3(p):
    '''help_star : empty'''
    p[0] = []

# for
def p_for_stmt(p): # testlist not finish ???
    'for_stmt : FOR ID IN testlist COLON suite'
    p[0] = For(AssName(p[2], 'OP_ASSIGN'), p[4], Stmt(p[6]), None)
    #print p[4]

def p_exprlist_1(p):
    '''exprlist : expr'''
    p[0] = [p[1]]

def p_exprlist_2(p):
    '''exprlist : exprlist COMMA expr'''
    p[0] = p[1] + [p[3]]

def p_testlist_1(p):
    '''testlist : test'''
    p[0] = p[1]

def p_testlist_2(p):
    '''testlist : testlist COMMA test'''
    a = []
    if isinstance(p[1], Tuple): 
        for tr in p[1]:
            a = a + [tr]
    else:
        a = [p[1]] + a
    a = a + [p[3]]
    p[0] = Tuple(a)
    #print p[0]

# expr
def p_expr(p): # xor_expr (VBAR xor_expr)*
    '''expr : xor_expr VBAR_xor_expr_star'''
    t = p[1]
    for tr in p[2]:
        if isinstance(tr, Bitor):
            tr.nodes.append(t)
            t = tr
    p[0] = t

def p_VBAR_xor_expr_star_1(p):
    '''VBAR_xor_expr_star : VBAR_xor_expr_star VBAR_xor_expr'''
    p[0] = p[1] + p[2]

def p_VBAR_xor_expr(p):
    '''VBAR_xor_expr : VBAR xor_expr'''
    p[0] = Bitor(p[2])

def p_VBAR_xor_expr_star_2(p):
    '''VBAR_xor_expr_star : empty'''
    p[0] = []

def p_xor_expr(p): #and_expr (CIRCUMFLEX and_expr)*
    '''xor_expr : and_expr CIRCUMFLEX_and_expr_star'''
    t = p[1]
    for tr in p[2]:
        if isinstance(tr, Bitxor):
            tr.nodes.append(t)
            t = tr
    p[0] = t

def p_CIRCUMFLEX_and_expr_star_1(p): 
    '''CIRCUMFLEX_and_expr_star : CIRCUMFLEX_and_expr_star CIRCUMFLEX_and_expr'''
    p[0] = p[1] + p[2]

def p_CIRCUMFLEX_and_expr(p):
    '''CIRCUMFLEX_and_expr : CIRCUMFLEX and_expr'''
    p[0] = Bitxor(p[2])

def p_CIRCUMFLEX_and_expr_star_2(p): 
    '''CIRCUMFLEX_and_expr_star : empty'''
    p[0] = []

def p_and_expr(p): #shift_expr (AMPER shift_expr)*
    '''and_expr : shift_expr AMPER_shift_expr_star'''
    t = p[1]
    for tr in p[2]:
        if isinstance(tr, Bitand):
            tr.nodes.append(t)
            t = tr
    p[0] = t
    
def p_AMPER_shift_expr_star_1(p):
    '''AMPER_shift_expr_star : AMPER_shift_expr_star AMPER_shift_expr'''
    p[0] = p[1] + p[2]

def p_AMPER_shift_expr(p):
    '''AMPER_shift_expr : AMPER shift_expr'''
    p[0] = Bitand(p[2])
    
def p_AMPER_shift_expr_star_2(p):
    '''AMPER_shift_expr_star : empty'''
    p[0] = []

def p_shift_expr(p): #arith_expr ((LEFTSHIFT|RIGHTSHIFT) arith_expr)*
    '''shift_expr : arith_expr SHIFT_arith_expr_star'''
    t = p[1]
    for tr in p[2]:
        if isinstance(tr, LeftShift):
            tr.left = t
            t = tr
        elif isinstance(tr, RightShift):
            tr.left = t
            t = tr
    p[0] = t
 
def p_SHIFT_arith_expr_star_1(p):
    '''SHIFT_arith_expr_star : SHIFT_arith_expr_star LEFTSHIFT_arith_expr '''
    p[0] = p[1] + p[2]

def p_LEFTSHIFT_arith_expr(p):
    '''LEFTSHIFT_arith_expr : LEFTSHIFT arith_expr'''
    p[0] = LeftShift(None,p[2])

def p_SHIFT_arith_expr_star_2(p): 
    '''SHIFT_arith_expr_star : SHIFT_arith_expr_star RIGHTSHIFT_arith_expr '''
    p[0] = p[1] + p[2]

def p_RIGHTSHIFT_arith_expr(p):
    '''RIGHTSHIFT_arith_expr : RIGHTSHIFT arith_expr'''
    p[0] = RightShift(None,p[2])

def p_SHIFT_arith_expr_star_3(p): 
    '''SHIFT_arith_expr_star : empty'''
    p[0] = []

def p_arith_expr(p): #term ((PLUS|MINUS) term)*
    '''arith_expr : term PM_term_star'''
    t = p[1]
    for tr in p[2]:
        if isinstance(tr, Add):
            tr.left = t
            t = tr
        elif isinstance(tr, Sub):
            tr.left = t
            t = tr
    p[0] = t

def p_PM_term_star_1(p):
    '''PM_term_star : PM_term_star PLUS_term
                    | PM_term_star MINUS_term'''
    p[0] = p[1] + p[2]
    
def p_PM_term_star_2(p):
    '''PM_term_star : empty'''
    p[0] = []


def p_PLUS_term(p):
    '''PLUS_term : PLUS term'''
    p[0] = [Add([None,p[2]])]

def p_MINUS_term(p):
    '''MINUS_term : MINUS term'''
    p[0] = [Sub([None,p[2]])]
    
def p_term_stmt(p): #factor ((STAR | SLASH | PERCENT | DOUBLESLASH ) factor)*
    # we can see that the * / % // are in the same level
    '''term : factor XX_factor_star'''
    t = p[1]
    for tr in p[2]:
        if isinstance(tr, Mul):
            tr.left = t
            t = tr
        elif isinstance(tr, Div):
            tr.left = t
            t = tr
        elif isinstance(tr, Mod):
            tr.left = t
            t = tr
    p[0] = t

def p_XX_factor_star_1(p):
    '''XX_factor_star : XX_factor_star STAR_factor
                      | XX_factor_star SLASH_factor
                      | XX_factor_star PERCENT_factor
                      | XX_factor_star DOUBLESLASH_factor'''
    p[0] = p[1] + p[2]

def p_XX_factor_star_2(p):
    '''XX_factor_star : empty'''
    p[0] = []

def p_SLASH_factor(p):
    '''SLASH_factor : SLASH factor'''
    p[0] = [Div([None,p[2]])]

def p_PERCENT_factor(p):
    '''PERCENT_factor : PERCENT factor'''
    p[0] = [Mod([None,p[2]])]

def p_DOUBLESLASH_factor(p):
    '''DOUBLESLASH_factor : DOUBLESLASH factor'''
    p[0] = [Div([None,p[2]])]

def p_STAR_factor(p):
    '''STAR_factor : STAR factor'''
    p[0] = [Mul([None,p[2]])]


# Write here~~~~~~~~~~~~~~




def p_factor_stmt_1(p):
    '''factor : PLUS factor'''
    p[0] = UnaryAdd(p[2])

def p_factor_stmt_2(p):
    '''factor : MINUS factor'''
    p[0] = UnarySub(p[2])

def p_factor_stmt_3(p):
    '''factor : TILDE factor'''
    p[0] = Invert(p[2])

def p_factor_stmt_4(p):
    '''factor : power'''
    p[0] = p[1]
    
    
def p_power(p): # atom (trailer)* (DOUBLESTAR factor)?
    '''power : atom trailer_star'''
    t = p[1]
    for tr in p[2]:
        if isinstance(tr, CallFunc):
            tr.node = t
            t = tr
        else:
            tr.expr = t
            t = tr
    p[0] = t
    
    
# BACKQUOTE testlist BACKQUOT
# as we set, atom can be:
# Tuple
# List
# Const
# [String, String, ...]
def p_atom_1(p):  
    '''atom : LPAREN RPAREN'''
    p[0] = Tuple(())

def p_atom_2(p): 
    '''atom : LBRACK RBRACK'''
    p[0] = List(())

def p_atom_3(p): 
    '''atom : INT
            | LONGINT
            | FLOAT'''
    p[0] = Const(p[1])

def p_atom_4(p): 
    '''atom : ID'''
    p[0] = Name(p[1])
    
def p_atom_5(p): # (STRING)+
    '''atom : STRING STRING_star'''    
    p[0] = Const(p[1] + p[2])

def p_string_star_1(p):
    '''STRING_star : empty'''  
    #p[0] = [Const('')]
    p[0] = ''

def p_string_star_2(p):
    '''STRING_star : STRING_star STRING'''
    p[0] = p[1] + p[2] # we set STRING_star a list
    
# we set trailer a list
# and trailer_star is a list consist of several trailers
def p_trailer_star_1(p):
    '''trailer_star : trailer_star trailer'''
    p[0] = p[1] + [p[2]]
    
def p_trailer_star_2(p):
    '''trailer_star : empty'''
    p[0] = []
    
# we set trailer is a list
def p_trailer_1(p):
    '''trailer : LPAREN RPAREN'''
    p[0] = CallFunc(None, [])
    
def p_trailer_2(p):
    '''trailer : LPAREN arglist RPAREN'''
    p[0] = CallFunc(None, p[2]) # arglist is already a list
    
#def p_trailer_3(p):
#    '''trailer : LBRACK subscriptlist RBRACK'''
#    p[0] = p[2]

def p_trailer_4(p):
    '''trailer : DOT ID'''
    p[0] = Getattr(None, p[2])

# Dang fan said we only use DOUBLESTAR in power, so we change grammar as follows:
#arglist : argument (COMMA argument)*
#          ( COMMA
#            ( STAR test)?
#          )?
def p_arglist_5(p):
    '''arglist : argument comma_argument_star'''
    p[0] = p[1] + p[2]
   
def p_comma_argument_star_1(p):
    '''comma_argument_star : comma_argument_star COMMA argument'''
    p[0] = p[1] + p[3]
    
def p_comma_argument_star_2(p):
    '''comma_argument_star : empty'''
    p[0] = []
    
def p_argument_1(p):
    '''argument : test ASSIGN test'''
    tr = p[1]
    if isinstance(tr, Getattr):
        p[0] = Assign([AssAttr(tr.expr,tr.attrname,'OP_ASSIGN')],p[3])
    elif isinstance(tr, Name):
        p[0] = Assign([AssName(tr.name, 'OP_ASSIGN')], p[3])
    #print "353" + p[0]
    
def p_argument_2(p):
    '''argument : test''' 
    p[0] = [p[1]]

  
def p_subscriptlist(p):
    '''subscriptlist : subscript COMMA_subscript_star COMMA
                     | subscript COMMA_subscript_star'''
    p[0] = p[1] + p[2]
    
def p_COMMA_subscript_star_1(p):
    '''COMMA_subscript_star : COMMA_subscript_star COMMA subscript'''
    p[0] = p[1] + p[3]

def p_COMMA_subscript_star_2(p):
    '''COMMA_subscript_star : empty'''
    p[0] = []
    
def p_subscript(p):
    '''subscript : DOT DOT DOT
                 | test COLON test sliceop
                 | test COLON test
                 | test COLON sliceop
                 | test COLON
                 | test
                 | COLON test sliceop
                 | COLON test
                 | COLON sliceop
                 | COLON'''
    
def p_sliceop(p):
    '''sliceop : COLON test
               | COLON'''
               
               
# expr_stmt               
def p_expr_stmt_1(p):
    '''expr_stmt : testlist augassign testlist'''
    p[0] = AugAssign(p[1],p[2],p[3])

def p_expr_stmt_2(p):
    '''expr_stmt : testlist assigns'''
    tr = p[1]
    if isinstance(tr, Getattr):
        p[0] = Assign([AssAttr(tr.expr,tr.attrname,'OP_ASSIGN')],p[2])
    elif isinstance(tr, Name):
        p[0] = Assign([AssName(tr.name, 'OP_ASSIGN')], p[2])
    elif isinstance(tr, Tuple):
        a = []
        for i in p[1]:
            a = a + [AssName(i.name,'OP_ASSIGN')]
        a = AssTuple(a)
        p[0] = Assign([a], p[2])
    #print "399"
    #print p[0]
    
def p_expr_stmt_3(p):
    '''expr_stmt : testlist'''
    p[0] = p[1]

def p_augassign(p):
    '''augassign : PLUSEQUAL
          | MINUSEQUAL
          | STAREQUAL
          | SLASHEQUAL
          | PERCENTEQUAL
          | AMPEREQUAL
          | VBAREQUAL
          | CIRCUMFLEXEQUAL
          | LEFTSHIFTEQUAL
          | RIGHTSHIFTEQUAL
          | DOUBLESTAREQUAL'''
    p[0] = p[1]

def p_assigns_1(p):
    '''assigns : ASSIGN testlist'''
    p[0] = p[2]

def p_assigns_2(p):
    '''assigns : assigns ASSIGN testlist'''
    tr = p[1]
    if isinstance(tr, Getattr):
        p[0] = Assign([AssAttr(tr.expr,tr.attrname,'OP_ASSIGN')],p[3])
    elif isinstance(tr, Name):
        p[0] = Assign([AssName(tr.name, 'OP_ASSIGN')], p[3])
    
# test:
def p_test_stmt(p): # set priority
    'test : or_test'
    p[0] = p[1]
    
def p_or_test(p): # or_test : and_test (OR and_test)*
    '''or_test : and_test or_and_test_Star'''
    t = p[1]
    for tr in p[2]:
        if tr is Or:
            tr.nodes.append(t)
            t = tr
    p[0] = t
    
def p_or_and_test_Star_1(p): #(OR and_test)*
    '''or_and_test_Star : or_and_test_Star OR_and_test'''
    p[0] = p[1] + p[2]

def p_OR_and_test(p):
    '''OR_and_test : OR and_test'''
    p[0] = Or(p[2])
    
def p_or_and_test_Star_2(p): #(OR and_test)*
    '''or_and_test_Star : empty'''
    p[0] = []
    
def p_and_test(p): # and_test : not_test (AND not_test)*
    '''and_test : not_test and_not_test_Star'''
    t = p[1]
    for tr in p[2]:
        if tr is And:
            tr.nodes.append(t)
            t = tr
    p[0] = t
        
def p_and_not_test_Star_1(p): # (AND not_test)*
    '''and_not_test_Star : and_not_test_Star AND_not_test'''
    p[0] = p[1] + p[2]

def p_AND_not_test(p):
    '''AND_not_test : AND not_test'''
    p[0] = And(p[2])
    
def p_and_not_test_Star_2(p): # (AND not_test)*
    '''and_not_test_Star : empty'''
    p[0] = [] # None for Name or Campare
    
def p_not_test_1(p):
    '''not_test : NOT not_test'''
    p[0] = Not(p[2])
    
def p_not_test_2(p):
    '''not_test : comparison''' 
    p[0] = p[1]
    
def p_comparison(p): # comparison : expr (comp_op expr)?
    '''comparison : expr comp_op_expr_Qmark'''
    #p[0] = Compare(Name(p[1]), p[2])
    if p[2] == None:
        p[0] = p[1]
    else:
        p[0] = Compare(p[1], p[2])
        
def p_comp_op_expr_Qmark_1(p): # (comp_op expr)?
    '''comp_op_expr_Qmark : comp_op expr'''
    p[0] = [(p[1], p[2])]
    
def p_comp_op_expr_Qmark_2(p): # (comp_op expr)?
    '''comp_op_expr_Qmark : empty'''
    p[0] = None

def p_comp_op(p):
    '''comp_op : LESS
    | GREATER
    | EQUAL
    | GREATEREQUAL
    | LESSEQUAL
    | ALT_NOTEQUAL
    | NOTEQUAL
    | IN
    | NOT IN
    | IS
    | IS NOT
    '''
    p[0] = p[1]
    
# funcdef : 'def' NAME parameters COLON suite
def p_funcdef(p):
    '''funcdef : DEF ID parameters COLON suite'''
    argnames = []
    defaults = []
    for i in p[3]:
        argnames += i.nodes[0]
        defaults += i.nodes[1]
    p[0] = Function(None, p[2], argnames, defaults, 0, None, Stmt(p[5]))
    
def p_parameters(p): # parameters : LPAREN (varargslist)? RPAREN
    '''parameters : LPAREN varargslist_Qmark RPAREN'''
    # Liu Jiaqi define parameters as a list.
    p[0] = p[2]
    
def p_varargslist_Qmark_1(p):
    '''varargslist_Qmark : varargslist'''
    p[0] = p[1]
    
def p_varargslist_Qmark_2(p):
    '''varargslist_Qmark : empty'''
    p[0] = []
    
def p_varargslist(p): # not finished, STAR do not process.
#    varargslist : defparameter (COMMA defparameter)*
#                (COMMA
#                    ( STAR NAME (COMMA DOUBLESTAR NAME)?
#                    | DOUBLESTAR NAME
#                    )?
#                )?
#                | STAR NAME (COMMA DOUBLESTAR NAME)?
#                | DOUBLESTAR NAME
    '''varargslist : defparameter COMMA_defparameter_Star'''
    p[0] = [p[1]] + p[2]
    
def p_COMMA_defparameter_Star_1(p):
    '''COMMA_defparameter_Star : COMMA_defparameter_Star COMMA defparameter'''
    # return list
    p[0] = p[1] + [p[3]]

def p_COMMA_defparameter_Star_2(p):
    '''COMMA_defparameter_Star : empty'''
    p[0] = []
    
def p_defparameter(p): # defparameter : fpdef (ASSIGN test)?
    '''defparameter : fpdef ASSIGN_test_Qmark'''
    a = Tuple(p[1])
    b = Tuple(p[2])
    p[0] = Tuple([a] + [b])
    
def p_ASSIGN_test_Qmark_1(p):
    '''ASSIGN_test_Qmark : ASSIGN test'''
    p[0] = [p[2]]
    
def p_ASSIGN_test_Qmark_2(p):
    '''ASSIGN_test_Qmark : empty'''
    p[0] = []
    
def p_fpdef(p): # do not finish fplist
    # fpdef : ID | LPAREN fplist RPAREN
    '''fpdef : ID '''
    p[0] = [p[1]]
    
# while
def p_while_stmt(p): # WHILE test COLON suite ('else' COLON suite)?
    '''while_stmt : WHILE test COLON suite else_COLON_suite_Qmark'''
    p[0]= While(p[2],Stmt(p[4]),p[5])
    
# commonly used
def p_COMMA_Qmark_1(p):    
    '''COMMA_Qmark : COMMA'''
    p[0] = p[1]

def p_COMMA_Qmark_2(p):    
    '''COMMA_Qmark : empty'''
    p[0] = None
    
def p_SEMI_Qmark(p):# (SEMI)?   
    '''SEMI_Qmark : SEMI
    | empty
    ''' 
  
# suite
def p_suite_1(p):
    '''suite : simple_stmt'''
    p[0] = p[1]
    
def p_suite_2(p):
    '''suite : NEWLINE INDENT stmt_PLUS DEDENT'''
    p[0] = p[3]
    
def p_stmt_PLUS_1(p):
    '''stmt_PLUS : stmt_PLUS stmt'''
    p[0] = p[1] + p[2]

def p_stmt_PLUS_2(p):
    '''stmt_PLUS : stmt'''
    p[0] = p[1]
    
# stmt
def p_stmt_1(p): # not finish
    # stmt : simple_stmt | compound_stmt
    '''stmt : simple_stmt'''
    p[0] = p[1]
    
def p_stmt_2(p): # not finish
    # stmt : simple_stmt | compound_stmt
    '''stmt : compound_stmt''' 
    p[0] = p[1]
    
def p_simple_stmt(p): # not write (SEMI small_stmt)*, write this: small_stmt (SEMI)? NEWLINE
    # small_stmt (SEMI small_stmt)* (SEMI)? NEWLINE
    '''simple_stmt : small_stmt SEMI_small_stmt_star SEMI_Qmark NEWLINE'''
    p[0] = p[1] + p[2]

def p_SEMI_small_stmt_star_1(p):
    '''SEMI_small_stmt_star : SEMI_small_stmt_star SEMI small_stmt'''
    p[0] = p[1] + p[3]

def p_SEMI_small_stmt_star_2(p):
    '''SEMI_small_stmt_star : empty'''
    p[0] = []


def p_small_stmt(p): # not finish
#small_stmt : expr_stmt
#           | print_stmt
#           | del_stmt
#           | pass_stmt
#           | flow_stmt
#           | import_stmt
#           | global_stmt
#           | exec_stmt
#           | assert_stmt
    '''small_stmt : print_stmt
                  | expr_stmt
                  | flow_stmt'''
    p[0] = [p[1]]
    
def p_flow_stmt(p):
    '''flow_stmt : break_stmt
                 | continue_stmt
                 | return_stmt'''
    p[0] = p[1]

def p_break_stmt(p):
    '''break_stmt : BREAK'''
    p[0] = Break(None)
    
def p_continue_stmt(p):
    '''continue_stmt : CONTINUE'''
    p[0] = Continue(None)

def p_return_stmt_1(p):
    '''return_stmt : RETURN testlist'''
    p[0] = Return(p[2])

def p_return_stmt_2(p):
    '''return_stmt : RETURN'''
    p[0] = Return(None)
    
def p_compound_stmt(p):
#             if_stmt
#              | while_stmt
#              | for_stmt
#              | try_stmt
#              | with_stmt
#              | funcdef
#              | classdef#
    '''compound_stmt : if_stmt
                     | while_stmt
                     | funcdef
                     | for_stmt
                     | classdef'''
    p[0] = [p[1]]
    #print p[1]
     
# if
def p_if_stmt(p):
    '''if_stmt : IF test COLON suite elif_clause_Star else_COLON_suite_Qmark'''
    a = []
    b = (p[2],Stmt(p[4]))
    a.append(b)
    for tr in p[5]:
        a.append(tr)
    p[0] = If(a,Stmt(p[6]))
    
def p_elif_clause_Star_1(p): # elif_clause*
    '''elif_clause_Star : elif_clause_Star elif_clause'''
    p[0] = p[1] + [p[2]]
    
def p_elif_clause_Star_2(p): # elif_clause*
    '''elif_clause_Star : empty'''
    p[0] = []
   
def p_elif_clause(p):
    '''elif_clause : ELIF test COLON suite'''
    p[0] = (p[2],Stmt(p[4]))

def p_else_COLON_suite_Qmark_1(p): # ('else' COLON suite)?
    '''else_COLON_suite_Qmark : ELSE COLON suite'''
    p[0] = p[3]

def p_else_COLON_suite_Qmark_2(p): # ('else' COLON suite)?
    '''else_COLON_suite_Qmark : empty'''
    p[0] = []
    
# print
def p_print_stmt(p): # do not write RIGHTSHIFT
    '''print_stmt : PRINT test COMMA_test_Star COMMA_Qmark'''
    a = [p[2]] + p[3]
    if p[4] is None:
        p[0] = Printnl(a,None)
    else:
        p[0] = Print(a,None)
    
def p_COMMA_test_Star_1(p):
    '''COMMA_test_Star : COMMA_test_Star COMMA test'''
    p[0] = p[1]+[p[3]]

def p_COMMA_test_Star_2(p):
    '''COMMA_test_Star : empty'''
    p[0] = []
# class
def p_classdef_1(p):
    '''classdef : CLASS ID LPAREN testlist RPAREN COLON suite'''
    p[0] = Class(p[2],[p[4]],None,Stmt(p[7]))
    
def p_classdef_2(p):
    '''classdef : CLASS ID LPAREN RPAREN COLON suite'''
    p[0] = Class(p[2],[],None,Stmt(p[6]))

def p_classdef_3(p):
    '''classdef : CLASS ID COLON suite'''
    p[0] = Class(p[2],[],None,Stmt(p[4]))

def p_empty(p):
    'empty :'

def p_error(p):
    print "Syntax error in input"
    
pyParser = yacc.yacc()