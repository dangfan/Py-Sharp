def flatten(seq):
    l = []
    for elt in seq:
        t = type(elt)
        if t is tuple or t is list:
            for elt2 in flatten(elt):
                l.append(elt2)
        else:
            l.append(elt)
    return l

def flatten_nodes(seq):
    return [n for n in flatten(seq) if isinstance(n, Node)]

class Node:
    """Abstract base class for ast nodes."""
    def getChildren(self):
        pass # implemented by subclasses
    def __iter__(self):
        for n in self.getChildren():
            yield n
    def getChildNodes(self):
        pass # implemented by subclasses

class Add(Node):
    def __init__(self, leftright):
        self.left = leftright[0]
        self.right = leftright[1]

    def getChildren(self):
        return self.left, self.right

    def getChildNodes(self):
        return self.left, self.right

class And(Node):
    def __init__(self, nodes):
        self.nodes = nodes

    def getChildren(self):
        return tuple(flatten(self.nodes))

    def getChildNodes(self):
        nodelist = []
        nodelist.extend(flatten_nodes(self.nodes))
        return tuple(nodelist)

class AssAttr(Node):
    def __init__(self, expr, attrname, flags):
        self.expr = expr
        self.attrname = attrname
        self.flags = flags

    def getChildren(self):
        return self.expr, self.attrname, self.flags

    def getChildNodes(self):
        return self.expr,

class AssName(Node):
    def __init__(self, name, flags):
        self.name = name
        self.flags = flags

    def getChildren(self):
        return self.name, self.flags

    def getChildNodes(self):
        return ()

class AssTuple(Node):
    def __init__(self, nodes):
        self.nodes = nodes

    def getChildren(self):
        return tuple(flatten(self.nodes))

    def getChildNodes(self):
        nodelist = []
        nodelist.extend(flatten_nodes(self.nodes))
        return tuple(nodelist)

class Assign(Node):
    def __init__(self, nodes, expr):
        self.nodes = nodes
        self.expr = expr

    def getChildren(self):
        children = []
        children.extend(flatten(self.nodes))
        children.append(self.expr)
        return tuple(children)

    def getChildNodes(self):
        nodelist = []
        nodelist.extend(flatten_nodes(self.nodes))
        nodelist.append(self.expr)
        return tuple(nodelist)

class AugAssign(Node):
    def __init__(self, node, op, expr):
        self.node = node
        self.op = op
        self.expr = expr

    def getChildren(self):
        return self.node, self.op, self.expr

    def getChildNodes(self):
        return self.node, self.expr

class Bitand(Node):
    def __init__(self, nodes):
        self.nodes = nodes

    def getChildren(self):
        return tuple(flatten(self.nodes))

    def getChildNodes(self):
        nodelist = []
        nodelist.extend(flatten_nodes(self.nodes))
        return tuple(nodelist)

class Bitor(Node):
    def __init__(self, nodes):
        self.nodes = nodes

    def getChildren(self):
        return tuple(flatten(self.nodes))

    def getChildNodes(self):
        nodelist = []
        nodelist.extend(flatten_nodes(self.nodes))
        return tuple(nodelist)

class Bitxor(Node):
    def __init__(self, nodes):
        self.nodes = nodes

    def getChildren(self):
        return tuple(flatten(self.nodes))

    def getChildNodes(self):
        nodelist = []
        nodelist.extend(flatten_nodes(self.nodes))
        return tuple(nodelist)

class Break(Node):
    def __init__(self):
        pass

    def getChildren(self):
        return ()

    def getChildNodes(self):
        return ()

class CallFunc(Node):
    def __init__(self, node, args):
        self.node = node
        self.args = args

    def getChildren(self):
        children = []
        children.append(self.node)
        children.extend(flatten(self.args))
        return tuple(children)

    def getChildNodes(self):
        nodelist = []
        nodelist.append(self.node)
        nodelist.extend(flatten_nodes(self.args))
        return tuple(nodelist)

class Class(Node):
    def __init__(self, name, bases, doc, code):
        self.name = name
        self.bases = bases
        self.doc = doc
        self.code = code

    def getChildren(self):
        children = []
        children.append(self.name)
        children.extend(flatten(self.bases))
        children.append(self.doc)
        children.append(self.code)
        return tuple(children)

    def getChildNodes(self):
        nodelist = []
        nodelist.extend(flatten_nodes(self.bases))
        nodelist.append(self.code)
        return tuple(nodelist)

class Compare(Node):
    def __init__(self, expr, ops):
        self.expr = expr
        self.ops = ops

    def getChildren(self):
        children = []
        children.append(self.expr)
        children.extend(flatten(self.ops))
        return tuple(children)

    def getChildNodes(self):
        nodelist = []
        nodelist.append(self.expr)
        nodelist.extend(flatten_nodes(self.ops))
        return tuple(nodelist)

class Const(Node):
    def __init__(self, value):
        self.value = value

    def getChildren(self):
        return self.value,

    def getChildNodes(self):
        return ()

class Continue(Node):
    def __init__(self):
        pass

    def getChildren(self):
        return ()

    def getChildNodes(self):
        return ()

    def __repr__(self):
        return "Continue()"

class Dict(Node):
    def __init__(self, items):
        self.items = items

    def getChildren(self):
        return tuple(flatten(self.items))

    def getChildNodes(self):
        nodelist = []
        nodelist.extend(flatten_nodes(self.items))
        return tuple(nodelist)

class Div(Node):
    def __init__(self, leftright):
        self.left = leftright[0]
        self.right = leftright[1]

    def getChildren(self):
        return self.left, self.right

    def getChildNodes(self):
        return self.left, self.right

class For(Node):
    def __init__(self, assign, list, body, else_):
        self.assign = assign
        self.list = list
        self.body = body
        self.else_ = else_

    def getChildren(self):
        children = []
        children.append(self.assign)
        children.append(self.list)
        children.append(self.body)
        children.append(self.else_)
        return tuple(children)

    def getChildNodes(self):
        nodelist = []
        nodelist.append(self.assign)
        nodelist.append(self.list)
        nodelist.append(self.body)
        if self.else_ is not None:
            nodelist.append(self.else_)
        return tuple(nodelist)

class Function(Node):
    def __init__(self, decorators, name, argnames, defaults, flags, doc, code):
        self.decorators = decorators
        self.name = name
        self.argnames = argnames
        self.defaults = defaults
        self.flags = flags
        self.doc = doc
        self.code = code

    def getChildren(self):
        children = []
        children.append(self.decorators)
        children.append(self.name)
        children.append(self.argnames)
        children.extend(flatten(self.defaults))
        children.append(self.flags)
        children.append(self.doc)
        children.append(self.code)
        return tuple(children)

    def getChildNodes(self):
        nodelist = []
        if self.decorators is not None:
            nodelist.append(self.decorators)
        nodelist.extend(flatten_nodes(self.defaults))
        nodelist.append(self.code)
        return tuple(nodelist)
    
class Getattr(Node):
    def __init__(self, expr, attrname):
        self.expr = expr
        self.attrname = attrname

    def getChildren(self):
        return self.expr, self.attrname

    def getChildNodes(self):
        return self.expr,

class If(Node):
    def __init__(self, tests, else_):
        self.tests = tests
        self.else_ = else_


    def getChildren(self):
        children = []
        children.extend(flatten(self.tests))
        children.append(self.else_)
        return tuple(children)

    def getChildNodes(self):
        nodelist = []
        nodelist.extend(flatten_nodes(self.tests))
        if self.else_ is not None:
            nodelist.append(self.else_)
        return tuple(nodelist)

class Invert(Node):
    def __init__(self, expr):
        self.expr = expr

    def getChildren(self):
        return self.expr,

    def getChildNodes(self):
        return self.expr,

class LeftShift(Node):
    def __init__(self, leftright):
        self.left = leftright[0]
        self.right = leftright[1]

    def getChildren(self):
        return self.left, self.right

    def getChildNodes(self):
        return self.left, self.right

class List(Node):
    def __init__(self, nodes):
        self.nodes = nodes

    def getChildren(self):
        return tuple(flatten(self.nodes))

    def getChildNodes(self):
        nodelist = []
        nodelist.extend(flatten_nodes(self.nodes))
        return tuple(nodelist)

class Mod(Node):
    def __init__(self, leftright):
        self.left = leftright[0]
        self.right = leftright[1]


    def getChildren(self):
        return self.left, self.right

    def getChildNodes(self):
        return self.left, self.right

class Module(Node):
    def __init__(self, doc, node):
        self.doc = doc
        self.node = node

    def getChildren(self):
        return self.doc, self.node

    def getChildNodes(self):
        return self.node,

class Mul(Node):
    def __init__(self, leftright):
        self.left = leftright[0]
        self.right = leftright[1]


    def getChildren(self):
        return self.left, self.right

    def getChildNodes(self):
        return self.left, self.right

class Name(Node):
    def __init__(self, name):
        self.name = name

    def getChildren(self):
        return self.name,

    def getChildNodes(self):
        return ()

class Not(Node):
    def __init__(self, expr):
        self.expr = expr


    def getChildren(self):
        return self.expr,

    def getChildNodes(self):
        return self.expr,

class Or(Node):
    def __init__(self, nodes):
        self.nodes = nodes

    def getChildren(self):
        return tuple(flatten(self.nodes))

    def getChildNodes(self):
        nodelist = []
        nodelist.extend(flatten_nodes(self.nodes))
        return tuple(nodelist)

class Pass(Node):
    def __init__(self):
        pass

    def getChildren(self):
        return ()

    def getChildNodes(self):
        return ()

class Power(Node):
    def __init__(self, leftright):
        self.left = leftright[0]
        self.right = leftright[1]

    def getChildren(self):
        return self.left, self.right

    def getChildNodes(self):
        return self.left, self.right

class Print(Node):
    def __init__(self, nodes, dest):
        self.nodes = nodes
        self.dest = dest

    def getChildren(self):
        children = []
        children.extend(flatten(self.nodes))
        children.append(self.dest)
        return tuple(children)

    def getChildNodes(self):
        nodelist = []
        nodelist.extend(flatten_nodes(self.nodes))
        if self.dest is not None:
            nodelist.append(self.dest)
        return tuple(nodelist)

class Printnl(Node):
    def __init__(self, nodes, dest):
        self.nodes = nodes
        self.dest = dest

    def getChildren(self):
        children = []
        children.extend(flatten(self.nodes))
        children.append(self.dest)
        return tuple(children)

    def getChildNodes(self):
        nodelist = []
        nodelist.extend(flatten_nodes(self.nodes))
        if self.dest is not None:
            nodelist.append(self.dest)
        return tuple(nodelist)

class Return(Node):
    def __init__(self, value):
        self.value = value

    def getChildren(self):
        return self.value,

    def getChildNodes(self):
        return self.value,

class RightShift(Node):
    def __init__(self, leftright):
        self.left = leftright[0]
        self.right = leftright[1]


    def getChildren(self):
        return self.left, self.right

    def getChildNodes(self):
        return self.left, self.right

class Set(Node):
    def __init__(self, nodes):
        self.nodes = nodes

    def getChildren(self):
        return tuple(flatten(self.nodes))

    def getChildNodes(self):
        nodelist = []
        nodelist.extend(flatten_nodes(self.nodes))
        return tuple(nodelist)

class Slice(Node):
    def __init__(self, expr, flags, lower, upper):
        self.expr = expr
        self.flags = flags
        self.lower = lower
        self.upper = upper

    def getChildren(self):
        children = []
        children.append(self.expr)
        children.append(self.flags)
        children.append(self.lower)
        children.append(self.upper)
        return tuple(children)

    def getChildNodes(self):
        nodelist = []
        nodelist.append(self.expr)
        if self.lower is not None:
            nodelist.append(self.lower)
        if self.upper is not None:
            nodelist.append(self.upper)
        return tuple(nodelist)

class Stmt(Node):
    def __init__(self, nodes):
        self.nodes = nodes

    def getChildren(self):
        return tuple(flatten(self.nodes))

    def getChildNodes(self):
        nodelist = []
        nodelist.extend(flatten_nodes(self.nodes))
        return tuple(nodelist)

class Sub(Node):
    def __init__(self, leftright):
        self.left = leftright[0]
        self.right = leftright[1]

    def getChildren(self):
        return self.left, self.right

    def getChildNodes(self):
        return self.left, self.right

class Subscript(Node):
    def __init__(self, expr, flags, subs):
        self.expr = expr
        self.flags = flags
        self.subs = subs

    def getChildren(self):
        children = []
        children.append(self.expr)
        children.append(self.flags)
        children.extend(flatten(self.subs))
        return tuple(children)

    def getChildNodes(self):
        nodelist = []
        nodelist.append(self.expr)
        nodelist.extend(flatten_nodes(self.subs))
        return tuple(nodelist)

class Tuple(Node):
    def __init__(self, nodes):
        self.nodes = nodes


    def getChildren(self):
        return tuple(flatten(self.nodes))

    def getChildNodes(self):
        nodelist = []
        nodelist.extend(flatten_nodes(self.nodes))
        return tuple(nodelist)

class UnaryAdd(Node):
    def __init__(self, expr):
        self.expr = expr


    def getChildren(self):
        return self.expr,

    def getChildNodes(self):
        return self.expr,

class UnarySub(Node):
    def __init__(self, expr):
        self.expr = expr


    def getChildren(self):
        return self.expr,

    def getChildNodes(self):
        return self.expr,

class While(Node):
    def __init__(self, test, body, else_):
        self.test = test
        self.body = body
        self.else_ = else_

    def getChildren(self):
        children = []
        children.append(self.test)
        children.append(self.body)
        children.append(self.else_)
        return tuple(children)

    def getChildNodes(self):
        nodelist = []
        nodelist.append(self.test)
        nodelist.append(self.body)
        if self.else_ is not None:
            nodelist.append(self.else_)
        return tuple(nodelist)
