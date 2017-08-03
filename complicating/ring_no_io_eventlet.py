#!/Library/Frameworks/Python.framework/Versions/2.5/bin/python
# encoding: utf-8
import sys
import eventlet

def run_benchmark(n, m):
    # print(">> Python 2.5.1, stackless 3.1b3 here (N=%d, M=%d)!\n" % (n, m))
    firstP = cin = eventlet.Queue()
    for s in xrange(1, n):
        seqn = s
        cout = eventlet.Queue()
        # print("*> s = %d" % (seqn, ))
        eventlet.spawn_n(loop, seqn, cin, cout)
        cin = cout
    else:
        seqn = s+1
        # print("$> s = %d" % (seqn, ))
    for r in xrange(m-1, -1, -1):
        # print("+ sending Msg#  %d" % r)
        firstP.put(r)
    mloop(seqn, cin)
def loop(s, cin, cout):
    while True:
        r = cin.get()
        cout.put(r)
        if r > 0: 
            # print(": Proc: <%s>, Seq#: %s, Msg#: %s .." % (pid(), s, r))
            pass
        else:
            # print("* Proc: <%s>, Seq#: %s, Msg#: terminate!" % (pid(), s))
            break
def mloop(s, cin):
    while True:
        r = cin.get()
        if r > 0: 
            # print("> Proc: <%s>, Seq#: %s, Msg#: %s .." % (pid(), s, r))
            pass
        else:
            # print("@ Proc: <%s>, Seq#: %s, ring terminated." % (pid(), s))
            break

def pid(): return eventlet.greenthread.getcurrent()

if __name__ == '__main__':
    run_benchmark(int(sys.argv[1]), int(sys.argv[2]))


