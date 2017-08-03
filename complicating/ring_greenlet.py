#!/Library/Frameworks/Python.framework/Versions/2.5/bin/python
# encoding: utf-8
import sys
from py.magic import greenlet

def run_benchmark(n, m):
    print(">> Python 2.5.1, stackless 3.1b3 here (N=%d, M=%d)!\n" % (n, m))
    glets = [greenlet.getcurrent()]
    for s in xrange(1, n):
        seqn = s
        glets.append(greenlet(loop))
        print("*> s = %d" % (seqn, ))
    else:
        seqn = s+1
        glets.append(greenlet(mloop))
        print("$> s = %d" % (seqn, ))
    glets[-1].switch(seqn, glets)
    for r in xrange(m-1, -1, -1):
        print("+ sending Msg#  %d" % r)
        glets[1].switch(r)
def loop(s, glets):
    previous = glets[s - 1]
    next = glets[s + 1]
    if s > 1:
        r = previous.switch(s - 1, glets)
    else:
        r = previous.switch()
    while True:
        if r > 0: 
            print(": Proc: <%s>, Seq#: %s, Msg#: %s .." % (pid("loop", s), s, r))
            pass
        else:
            print("* Proc: <%s>, Seq#: %s, Msg#: terminate!" % (pid("loop", s), s))
            break
        next.switch(r)
        r = previous.switch()
    next.switch(r)
def mloop(s, glets):
    previous = glets[s - 1]
    r = previous.switch(s - 1, glets)
    while True:
        if r > 0: 
            print("> Proc: <%s>, Seq#: %s, Msg#: %s .." % (pid("mloop", s), s, r))
            pass
        else:
            print("@ Proc: <%s>, Seq#: %s, ring terminated." % (pid("mloop", s), s))
            break
        r = previous.switch()

def pid(func, s): return "<<%s(Greenlet-%d, started)>>" % (func, s)

if __name__ == '__main__':
    run_benchmark(int(sys.argv[1]), int(sys.argv[2]))

