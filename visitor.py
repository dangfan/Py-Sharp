import json
from ast import *
import string

class Visitor:
    def __init__(self):
        self.indent = ''
        self.function_names = []  # global function table
        self.class_names = set([])     # global class table
        self.global_functions = []
        self.classes = []
        self.prefix = '_Main.'
        self.paras = []
        self.pyNames = ['str', 'xrange']
        
    def reset(self):
        self.indent = ''
        self.global_functions = []
        self.classes = []
        self.prefix = '_Main.'
        self.paras = []
        
    def generate(self, _ast):
        self.visit(_ast)
        self.reset()
        code = self.visit(_ast)
        code = code % ('\n'.join(self.global_functions), '\n'.join(self.classes))
        return code
    
    def visit(self, node, parent = None):
        '''Calls the appropriate visit function based on node type.
        Puts the result between parenthesis if parent is specified and precedence of node is less than that of parent.'''
        if node is None:
            return ''
        nodetype = node.__class__.__name__
        f = getattr(self, 'visit_' + nodetype, None) # get visit function
        if nodetype == 'Stmt':
            code = f(node, parent)
        elif f:
            code = f(node)                    # use a specified visit function
        else:
            code = self.visit_children(node)  # use a general visit function
        if code is None:
            code = ''                         # empty code
        elif isinstance(code, basestring):
            pass                              # a simple string, just use it
        else:
            code = ''.join(code)              # a list
        if parent and self.get_precedence(node) > self.get_precedence(parent):
            code = '(%s)' % code              # add parenthesis
        return code
    
    # syntactic sugar for calling visit
    __call__ = visit
    
    def get_precedence(self, node):
        precedence = {
            UnaryAdd : 0,
            UnarySub : 0,
            Not : 0,
            Invert : 0,
            Mul : 1,
            Div : 1,
            Mod : 1,
            Add : 2,
            Sub : 2,
            LeftShift : 3,
            RightShift : 3,
            Compare : 4,
            Bitand : 5,
            Bitxor : 6,
            Bitor : 7,
            And : 8,
            Or : 9,
        }
        return precedence.get(node.__class__, -1)
    
    def visit_children(self, node, sep = ' '):
        return sep.join(self.visit(n) for n in node.getChildNodes())
    
    # AST node visitors
    
    def visit_Add(self, node):
        return '%s + %s' % (self(node.left, node), self(node.right, node))
    
    def visit_And(self, node):
        return ' && '.join(self(n, node) for n in node.nodes)
    
    def visit_AssAttr(self, node):
        if isinstance(node.expr, Name):
            return self(node.expr) + '.' + node.attrname
        else:
            return '(%s).%s' % (self(node.expr), node.attrname)
    
    def visit_AssName(self, node):
        return self.prefix + node.name
    
    def visit_Assign(self, node):
        lst = []
        for na in node.nodes:
            lst.append(self.assign(na, node.expr))
        return '\n'.join(lst)
            
    def assign(self, node, expr):
        if isinstance(node, AssTuple):
            lst = []
            for i in xrange(0, len(node.nodes)):
                lst.append('%s = %s;' % (self(node.nodes[i]), self(expr.nodes[i])))
            return ' '.join(lst)[:-1]
        elif isinstance(node, Subscript):
            m = node.getChildNodes()[0]
            n = node.getChildNodes()[1]
            return '%s[%s] = %s' % (self(m), self(n), self(expr))
        else:
            return '%s = %s' % (self(node), self(expr))


    def visit_AugAssign(self, node):
        left = node.node
        right = node.expr
        return '%s %s %s' % (self(left), node.op, self(right))

    def visit_Bitand(self, node):
        return ' & '.join(self(n, node) for n in node.nodes)

    def visit_Bitor(self, node):
        return ' | '.join(self(n) for n in node.nodes)

    def visit_Bitxor(self, node):
        return ' ^ '.join(self(n, node) for n in node.nodes)
    
    def visit_Break(self, node):
        return 'break'

    def visit_CallFunc(self, node):
        f = self(node.node)
        if f.startswith('self.'): f = f[5:]
        args = ', '.join(self(n) for n in node.args)
        return '%s(%s)' % (f, args)

    def visit_Class(self, node):
        nameline = node.name + ' : '
        self.class_names.add(node.name)
        if len(node.bases) == 1:
            nameline += self(node.bases[0])[4:] + ', '
        elif len(node.bases) > 1:
            raise 'Multiple inheritance not supported'
	nameline += 'IDynamicMetaObjectProvider'
        prefix = self.prefix
        self.prefix = 'self.'
        code = self(node.code, node)
        self.classes.append('''class %s
{
    DynamicMetaObject IDynamicMetaObjectProvider.GetMetaObject(
        System.Linq.Expressions.Expression parameter)
    {
        return new MetaObject(parameter, this);
    }
    private class MetaObject : DynamicMetaObject
    {
        internal MetaObject(
            System.Linq.Expressions.Expression parameter,
            %s value)
            : base(parameter, BindingRestrictions.Empty, value)
        {
        }
        public override DynamicMetaObject BindSetMember(SetMemberBinder binder,
            DynamicMetaObject value)
        {
            string methodName = "SetDictionaryEntry";
            BindingRestrictions restrictions =
                BindingRestrictions.GetTypeRestriction(Expression, LimitType);
            Expression[] args = new Expression[2];
            args[0] = Expression.Constant(binder.Name);
            args[1] = Expression.Convert(value.Expression, typeof(object));
            Expression self = Expression.Convert(Expression, LimitType);
            Expression methodCall = Expression.Call(self,
                    typeof(%s).GetMethod(methodName),
                    args);
            DynamicMetaObject setDictionaryEntry = new DynamicMetaObject(
                methodCall,
                restrictions);
            return setDictionaryEntry;
        }
        public override DynamicMetaObject BindGetMember(GetMemberBinder binder)
        {
            string methodName = "GetDictionaryEntry";
            Expression[] parameters = new Expression[]
            {
                Expression.Constant(binder.Name)
            };
            DynamicMetaObject getDictionaryEntry = new DynamicMetaObject(
                Expression.Call(
                    Expression.Convert(Expression, LimitType),
                    typeof(%s).GetMethod(methodName),
                    parameters),
                BindingRestrictions.GetTypeRestriction(Expression, LimitType));
            return getDictionaryEntry;
        }
    }
    private dynamic self = new ExpandoObject();
    public object SetDictionaryEntry(string key, object value)
    {
        var t = (IDictionary<string, object>)self;
        if (t.ContainsKey(key))
            t[key] = value;
        else
            t.Add(key, value);
        return value;
    }
    public object GetDictionaryEntry(string key)
    {
        return ((IDictionary<string, object>)self)[key];
    }
    %s
}''' % (nameline, node.name, node.name, node.name, code))
        self.prefix = prefix

    def visit_Compare(self, node):
        if isinstance(node.ops[0][1], List) and node.ops[0][0] == "in":
            return '(Py.convert(%s)).Contains(Py.str(%s))' % (self(node.ops[0][1]), self(node.expr))
        elif isinstance(node.ops[0][1], List) and node.ops[0][0] == "not in":
            return '!(Py.convert(%s)).Contains(Py.str(%s))' % (self(node.ops[0][1]), self(node.expr))
        elif isinstance(node.ops[0][1], Tuple) and node.ops[0][0] == "in":
            return '(Py.convert(%s)).Contains(Py.str(%s))' % (self(node.ops[0][1]), self(node.expr))
        elif isinstance(node.ops[0][1], Tuple) and node.ops[0][0] == "not in":
            return '!(Py.convert(%s)).Contains(Py.str(%s))' % (self(node.ops[0][1]), self(node.expr))
        elif isinstance(node.ops[0][1], CallFunc) and node.ops[0][0] == "in":
            return '(Py.convert(%s)).Contains(Py.str(%s))' % (self(node.ops[0][1]), self(node.expr))
        elif isinstance(node.ops[0][1], CallFunc) and node.ops[0][0] == "not in":
            return '!(Py.convert(%s)).Contains(Py.str(%s))' % (self(node.ops[0][1]), self(node.expr))
        else:
            return '%s %s %s' % (self(node.expr), node.ops[0][0], self(node.ops[0][1]))
    
    def visit_Const(self, node):
        if isinstance(node.value, basestring):
            return json.dumps(node.value)
        else:
            return repr(node.value)

    def visit_Continue(self, node):
        return 'continue'
    
    def visit_Dict(self, node):
        return 'new Dictionary<object, object>{%s}' % (', '.join('{%s, %s}' % (self(n[0]), self(n[1])) for n in node.items))
    
    def visit_Div(self, node):
        return '%s / %s' % (self(node.left, node), self(node.right, node))
    
    def visit_For(self, node):
        yield 'foreach (dynamic %s in %s)\n' % (node.assign.name, self(node.list))
        yield self.indent + '{\n'
        self.indent += '    '
        self.paras.append(node.assign.name)  # remove prefix before loop variable
        yield self(node.body)
        self.indent = self.indent[4:]
        self.paras.pop()
        yield '\n' + self.indent + '}'

    def gen_paras(self, node):
        paralist = node.argnames[:]
        i = len(node.argnames) - len(node.defaults)
        for d in node.defaults:
            paralist[i] += ' = ' + self(d)
            i = i + 1
        inClass = False
        if len(paralist) > 0 and paralist[0] == 'self':
            paralist = paralist[1:]
            inClass = True
        return paralist, inClass

    def visit_Function(self, node):
        paralist, inClass = self.gen_paras(node)
        paras = ', '.join('dynamic ' + n for n in paralist)
        
        preparas = self.paras
        self.paras = node.argnames
        
        prefix = self.prefix
        self.prefix = '_%s.' % node.name
        
        self.isReturned = False
        self.indent = '        ' 
        code = self(node.code)
        self.indent = '    ' 
        ret_type = 'dynamic' if self.isReturned else 'void'
        
        fun = self.indent + 'public %s %s(%s)\n' % (ret_type, node.name, paras)\
              + self.indent + '{\n'\
              + self.indent + '    dynamic %s = new ExpandoObject();\n' % self.prefix[:-1]\
              + '%s\n' % code\
              + self.indent + '}'

        self.prefix = prefix
        self.praras = preparas
        self.indent = '        ' 
        
        if inClass:
            return fun
        else:
            self.function_names.append(node.name)
            self.global_functions.append('static ' + fun[4:])
    
    def visit_Getattr(self, node):
        return self.visit_AssAttr(node)
    
    def visit_If(self, node):
        lst = []
        for test in node.tests:
            self.indent += '    '
            lst.append(self.indent[4:] + 'else if (%s)\n' % self(test[0])\
                       + self.indent[4:] + '{\n%s\n' % self(test[1])\
                       + self.indent[4:] + '}')
            self.indent = self.indent[4:]
        if len(node.else_.nodes) > 0:
            self.indent += '    '
            lst.append(self.indent[4:] + 'else\n'\
                       + self.indent[4:] + '{\n%s\n' % self(node.else_)\
                       + self.indent[4:] + '}')
            self.indent = self.indent[4:]
        return '\n'.join(lst)[13:]
    
    def visit_Invert(self, node):
        return '~' + self(node.expr, node)

    def visit_LeftShift(self, node):
        return '%s << %s' % (self(node.left), self(node.right))

    def visit_List(self, node):
        return 'new PyList(){%s}' % (', '.join(self(n) for n in node.nodes))

    def visit_Mod(self, node):
        return '%s %% %s' % (self(node.left, node), self(node.right, node))
    
    def visit_Module(self, node):
        self.indent = '        '
        return '''using System;
using System.Collections.Generic;
using System.Dynamic;
using System.Linq;
using System.Linq.Expressions;
using System.Text;

static class Py
{
    public static string str(object o)
    {
        if (o == null)
            return "None";
        if (o is PyList)
            return "[" + string.Join(", ", convert(o as PyList)) + "]";
        return o.ToString();
    }
    public static List<string> convert(PyList lst)
    {
        var tmp = new List<string>();
        foreach (var t in lst)
        {
            if (t is string)
                tmp.Add(string.Format("'{0}'", t));
            else
                tmp.Add(t.ToString());
        }
        return tmp;
    }
    public static PyList range(int l, int h = -1, int s = 1)
    {
        if (h == -1)
        {
            h = l;
            l = 0;
        }
        var list = new PyList();
        for (int i = l; i < h; i += s)
            list.Add(i);
        return list;
    }
    public static PyList xrange(int l, int h = -1, int s = 1)
    {
        return range(l, h, s);
    }
    public static PyList slice(PyList lst, object l, object h)
    {
        int low, high;
        if (l == null)
            low = 0;
        else
            low = (int)l;
        if (h == null)
            high = lst.Count;
        else
            high = (int)h;
        var tmp = new PyList();
        for (int i = low; i < high; ++i)
            tmp.Add(lst[i]);
        return tmp;
    }
}
class PyList : List<object>
{
    public void append(object o)
    {
        this.Add(o);
    }
}
class Program
{
    static void Main(string[] args)
    {
        dynamic _Main = new ExpandoObject();
%s
    }
    %%s
}
%%s''' % self(node.node)
    
    def visit_Mul(self, node):
        return '%s * %s' % (self(node.left, node), self(node.right, node))
    
    def visit_Name(self, node):
        names = {
            'True': 'true',
            'False': 'false',
            'None': 'null'
        }
        if node.name in self.function_names + self.paras + ['self']:
            name = node.name
        elif node.name in self.class_names:
            name = 'new ' + node.name
        elif node.name in self.pyNames:
            name = 'Py.' + node.name
        else:
            name = self.prefix + node.name
        return names.get(node.name, name)

    def visit_Not(self, node):
        return '!' + self(node.expr, node)

    def visit_Or(self, node):
        return ' || '.join(self(n) for n in node.nodes)

    def visit_Pass(self, node):
        return ''

    def visit_Power(self, node):
        return 'Math.Pow(%s, %s)' % (self(node.left), self(node.right))

    def visit_Print(self, node):
        return ' Console.Write(" "); '.join('Console.Write(Py.str(%s));' % self(n) for n in node.nodes)

    def visit_Printnl(self, node):
        return ' Console.Write(" "); '.join('Console.Write(Py.str(%s));' % self(n) for n in node.nodes) + '\n' + self.indent + 'Console.WriteLine()'
    
    def visit_Return(self, node):
        self.isReturned = True
        return 'return %s' % self.visit(node.value)

    def visit_RightShift(self, node):
        return '%s >> %s' % (self(node.left), self(node.right))

    def visit_Slice(self, node):
        return 'Py.slice(%s, %s, %s)' % (self(node.expr),
                                        'null' if self(node.lower) == '' else self(node.lower),
                                        'null' if self(node.upper) == '' else self(node.upper))

    def visit_Stmt(self, node, parent = None):
        if not isinstance(parent, Class):
            tmp = ''
            for n in node.getChildNodes():
                tmp += self.indent + self(n)
                tmp += ';' if not isinstance(n, (If, While, Pass, For)) else ''
                tmp += '\n'
            return tmp[:-1]
        # deal with the statements right in a class
        funclst = []
        conslst = []
        hasInit = False
        for st in node.getChildNodes():
            if isinstance(st, Function):
                tmp = self(st)
                if st.name == '__init__':
                    hasInit = True
                    tmp = string.replace(tmp, '__init__', parent.name)
                    tmp = string.replace(tmp, 'void ', '')
                    pos = string.rfind(tmp, '}')
                    tmp = tmp[:pos] + '    __init__();\n' + self.indent[4:] + tmp[pos:]
                funclst.append(tmp)
            else:
                conslst.append(self(st))
        constructor = '''private void __init__()
    {
        %s;
    }
''' % (';\n'.join(conslst))
        if not hasInit:
            constructor = '''public %s()
    {
        __init__();
    }
''' % parent.name + constructor
        return constructor + '\n'.join(funclst)
    
    def visit_Sub(self, node):
        return '%s - %s' % (self(node.left, node), self(node.right, node))

    def visit_Subscript(self, node):
        return '%s[%s]' % (self(node.expr), self(node.subs[0]))

    def visit_Tuple(self, node):
        return self.visit_List(node)

    def visit_UnaryAdd(self, node):
        return "+" + self(node.expr, node)

    def visit_UnarySub(self, node):
        return "-" + self(node.expr, node)

    def visit_While(self, node):
        yield 'while (%s)\n' % self(node.test)
        yield self.indent + '{\n'
        self.indent += '    '
        yield self(node.body)
        self.indent = self.indent[4:]
        yield '\n' + self.indent + '}'
