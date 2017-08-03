#!/Library/Frameworks/Python.framework/Versions/2.5/bin/python
# encoding: utf-8
import sys
import stackless as SL

def run_benchmark(n, m):
    print(">> Python 2.5.1, stackless 3.1b3 here (N=%d, M=%d)!\n" % (n, m))
    firstP = cin = SL.channel()
    for s in xrange(1, n):
        seqn = s
        cout = SL.channel()
        print("*> s = %d" % (seqn, ))
        t = SL.tasklet(loop)(seqn, cin, cout)
        cin = cout
    else:
        seqn = s+1
        print("$> s = %d" % (seqn, ))
        t = SL.tasklet(mloop)(seqn, cin)
    for r in xrange(m-1, -1, -1):
        print("+ sending Msg#  %d" % r)
        firstP.send(r)
    SL.schedule()
def loop(s, cin, cout):
    while True:
        r = cin.receive()
        cout.send(r)
        if r > 0: 
            print(": Proc: <%s>, Seq#: %s, Msg#: %s .." % (pid(), s, r))
            pass
        else:
            print("* Proc: <%s>, Seq#: %s, Msg#: terminate!" % (pid(), s))
            break
def mloop(s, cin):
    while True:
        r = cin.receive()
        if r > 0: 
            print("> Proc: <%s>, Seq#: %s, Msg#: %s .." % (pid(), s, r))
            pass
        else:
            print("@ Proc: <%s>, Seq#: %s, ring terminated." % (pid(), s))
            break

def pid(): return repr(SL.getcurrent()).split()[-1][2:-1]

if __name__ == '__main__':
    run_benchmark(int(sys.argv[1]), int(sys.argv[2]))


