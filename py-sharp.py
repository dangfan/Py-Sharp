from lexer import lexer
from visitor import Visitor
from pyParser import pyParser
import sys
import platform
import os

filename = sys.argv[1]
output = sys.argv[2]
f = open(filename).read() + '\n'
ast = pyParser.parse(f, lexer=lexer)
f = open(output, 'w')
f.write(Visitor().generate(ast))
f.close()

if platform.system() == 'Linux':
    os.system('mono-csc ' + output)
else:
    os.system('csc ' + output)