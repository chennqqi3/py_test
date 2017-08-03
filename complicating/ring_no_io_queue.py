#!/Library/Frameworks/Python.framework/Versions/2.5/bin/python
# encoding: utf-8
import sys
import threading, Queue

def run_benchmark(n, m):
    # print(">> Python 2.5.1, stackless 3.1b3 here (N=%d, M=%d)!\n" % (n, m))
    firstP = cin = Queue.Queue()
    for s in xrange(1, n):
        seqn = s
        cout = Queue.Queue()
        # print("*> s = %d" % (seqn, ))
        t = Loop(seqn, cin, cout)
        t.setDaemon(False)
        t.start()
        cin = cout
    else:
        seqn = s+1
        # print("$> s = %d" % (seqn, ))
        t = MLoop(seqn, cin)
        t.setDaemon(False)
        t.start()
    for r in xrange(m-1, -1, -1):
        # print("+ sending Msg#  %d" % r)
        firstP.put(r)
class Loop(threading.Thread):
    def __init__(self, s, cin, cout):
        threading.Thread.__init__(self)
        self.cin = cin
        self.cout = cout
        self.s = s
    def run(self):
        while True:
            r = self.cin.get()
            self.cout.put(r)
            if r > 0: 
                 # print(": Proc: <%s>, Seq#: %s, Msg#: %s .." % (pid(), self.s, r))
                 pass
            else:
                 # print("* Proc: <%s>, Seq#: %s, Msg#: terminate!" % (pid(), self.s))
                 break
class MLoop(threading.Thread):
    def __init__(self, s, cin):
        threading.Thread.__init__(self)
        self.cin = cin
        self.s = s
    def run(self):
        while True:
            r = self.cin.get()
            if r > 0: 
                # print("> Proc: <%s>, Seq#: %s, Msg#: %s .." % (pid(), self.s, r))
                pass
            else:
                # print("@ Proc: <%s>, Seq#: %s, ring terminated." % (pid(), self.s))
                break

def pid(): return threading.currentThread()

if __name__ == '__main__':
    run_benchmark(int(sys.argv[1]), int(sys.argv[2]))


