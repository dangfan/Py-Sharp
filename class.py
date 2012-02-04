class A:
    def __init__(self):
        self.a = 3
    def t(self):
        print self.a

class B(A):
    b = 3
    def test(self):
        self.t()
        print self.b

b = B()
b.test()
