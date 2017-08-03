class A(object):
    def __init__(self,a):
        print 'init A...'
        self.a = a


class B(A):
    def __init__(self,a,b):
        super(B, self).__init__(a)
        print 'init B...'
        self.b = b


class C(A):
    def __init__(self, a,c):
        super(C, self).__init__(a)
        print 'init C...'
        self.c = c


class D(B, C):
    def __init__(self, a ,d):
        (D, self).__init__
        print 'init D...'
        self.d = d


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)