# coding=utf-8

import poplib
import StringIO, email

def dcode(str):
    h = email.Header.Header(str)
    dh = email.Header.decode_header(h)
    return dh[0][0]

popsrv = "pop.xxxxxxxx.com"  #连接 登录 服务器
username = "hsbk@xxxxxx.com"
passwd = "123456"


subject=""
f_addr=""
f_name=""
to=[]
cc=[]
bc=[]

pop = poplib.POP3(popsrv)
pop.set_debuglevel(1)
pop.user(username)
pop.pass_(passwd)


num,total_size = pop.stat()
hdr,text,octet=pop.retr(num) #取最后封邮件
text = '\n'.join(text) #将list拼接成字串

amail = email.message_from_string(text)
subject = dcode(amail.get("subject"))



f_addr = email.utils.parseaddr(amail.get("from"))[1]
f_name = dcode(email.utils.parseaddr(amail.get("from"))[0])




tol=[]
tostr = msg.get('to')

if tostr == None :
    tostr = ''

tostr = tostr.replace('\n','').replace('\t','').replace('"','').replace("'","")
tol = tostr.split(',')
for t in tol:
    taddr = email.utils.parseaddr(t)[1]
    inx = taddr.find("@")
    if inx != -1:
        to.append(taddr)


tol=[]

tostr = msg.get('bc')

if tostr == None :
    tostr = ''

tostr = tostr.replace('\n','').replace('\t','').replace('"','').replace("'","")

tol = tostr.split(',')
for t in tol:
    taddr = email.utils.parseaddr(t)[1]
    inx = taddr.find("@")
    if inx != -1:
        bc.append(taddr)


tol=[]
tostr = msg.get('cc')

if tostr == None :
    tostr = ''

tostr = tostr.replace('\n','').replace('\t','').replace('"','').replace("'","")
tol = tostr.split(',')
for t in tol:
    taddr = email.utils.parseaddr(t)[1]
    inx = taddr.find("@")
    if inx != -1:
        cc.append(taddr)



fp = open('e:/test3.eml','wb')
fp.write(text)
fp.close()
#pop.dele(num) #删除服务器上的副本


print "subject ",subject
print "f_addr ",f_addr
print "f_name ",f_name
print "to ",to
print "cc ",cc
print "bc ",bc