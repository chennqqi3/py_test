# coding=utf-8

import sys
import json
import time
import smtplib
import poplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import MySQLdb
from sqlalchemy import create_engine


reload(sys)
sys.setdefaultencoding( "utf-8")

dev_db_url = 'mysql://admin:admin1234@192.168.5.87:3306/ndb?charset=utf8'

class SQLQuery(object):
    def __init__(self, engine):
        self.engine = engine
        self.record = {}
        self.lastInsertID = None
        self.affectedRows = None
        self.rowcount = None

    def Query(self, query):
        conn = self.engine.connect()
        try:
            result = conn.execute(query)
            if result.returns_rows:
                self.record = result
            self.affectedRows = result.rowcount
            self.rowcount = result.rowcount
            self.lastInsertID = result.lastrowid
        finally:
            if conn is not None:
                conn.close()

    def call_proc(self, query):
        connection = self.engine.raw_connection()
        try:
            cursor = connection.cursor()
            cursor.callproc(query)
            cursor.close()
            connection.commit()
        finally:
            connection.close()


def get_dev_query():
    return SQLQuery(create_engine(dev_db_url))

query = get_dev_query()


def insert_email(tmp_map):
    # print unicode(tmp_map["Subject"], "utf-8")
    # print unicode(tmp_map["from"], "utf-8")
    # print unicode(tmp_map["to"], "utf-8")
    if tmp_map["Subject"].find("[case:") != -1:
        print unicode(tmp_map["Subject"], "utf-8")
    # query.Query(
    #     "insert into ndb_email_record(subject, from, to)"
    #     "VALUES (%s, %s, %s) " %
    #     (unicode(tmp_map["Subject"], "utf-8"), unicode(tmp_map["from"], "utf-8"), unicode(tmp_map["to"], "utf-8")))


filePath = "email_info.log"


def send_mail(send_fromname,send_frompasw,text, files=None):
    print "\t send email"
    send_from = send_fromname
    #'dbsender@capvision.com'
    #send_from = '18201031103@163.com'
    #send_to = ['wmlu2004st@gmail.com','18201031103@139.com']
    send_to = ['41115149@qq.com','llu@capvision.com']
    subject = 'test from Python smtp25'

    msg = MIMEMultipart(
        From=send_from,
        To=COMMASPACE.join(send_to),
        Date=formatdate(localtime=True),
        Subject=subject
    )
    msg['Subject'] = subject
    msg['From'] = send_from
    msg['To'] = ','.join(send_to)
    content = MIMEText(text, 'plain', 'utf-8')
    msg.attach(content)

    for f in files or []:
        with open(f, "rb") as fil:
            msg.attach(MIMEApplication(
                fil.read(),
                # Content_Disposition='attachment; filename="%s"' % basename(f),
                # Name=basename(f)
            ))

    #smtp = smtplib.SMTP('smtp.office365.com',587)
    #smtp = smtplib.SMTP('partner.outlook.cn',25)
    smtp = smtplib.SMTP('smtp.partner.outlook.cn',587)
    #smtp = smtplib.SMTP_SSL('smtp.163.com',465)

    #smtp.login('18201031103@163.com', 'yiojudfgxzpkcmfq')
    smtp.starttls()
    #smtp.login('llu@capvision.com','Cap15715')
    smtp.login(send_fromname,send_frompasw)
    #'llu@capvision.com','Cap15715')
    #smtp.login('dbsender@capvision.com','1qaz@WSX')
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


email_info = {}


def recv_off365():
    try:
        pp=poplib.POP3_SSL('partner.outlook.cn', 995)
        pp.user('mailtondb@capvision.com')
        pp.pass_('1qaz@WSX')
        num = len(pp.list()[1])
        ret = pp.stat()
        for i in range(1, num):
            resp, lines, octets = pp.retr(i)
            msg_content = '\r\n'.join(lines)
            msg = Parser().parsestr(msg_content)
            print_info(email_info, msg, i)
            insert_email(print_info(email_info, msg, i))

        print email_info

        pp.quit()
    except poplib.error_proto, e:
        print "Login failed:", e
        sys.exit(1)


def print_info(email_info, msg, di, indent=0):
    email_info_tmp = {}
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header =='Subject':
                    value = decode_str(value)
                else:
                    try:
                        hdr, addr = parseaddr(value)
                        name = decode_str(hdr)
                        value = u'%s <%s>' % (name, addr)
                    except Exception, e:
                        print "zenmele", value
            file_object = open(filePath, "a")
            try:
                # print('%s%s: %s' % (' ' * indent, header, value))
                su = ('%s%s: %s' % (' ' * indent, header, value)).encode("utf-8")
                # su = ('%s%s: %s' % (' ' * indent, header, value))
                if su[0:5] == 'From:':
                    # print u'发件人: ', su[5:len(su)]
                    email_info_tmp.setdefault("from", "")
                    email_info_tmp["from"] = su[5:len(su)]
                if su[0:3] == 'To:':
                    # print u'收件人: ', su[3:len(su)]
                    email_info_tmp.setdefault("to", "")
                    email_info_tmp["to"] = su[3:len(su)]
                if su[0:8] == 'Subject:':
                    # print u'主题: ', su[8:len(su)]
                    email_info_tmp.setdefault("Subject", "")
                    email_info_tmp["Subject"] = su[8:len(su)]

                file_object.write("\n")
                file_object.write(su)
            except Exception, e:
                print "yichangle", hdr, addr
            finally:
                file_object.close()
    # if (msg.is_multipart()):
    #     parts = msg.get_payload()
    #     for n, part in enumerate(parts):
    #         # print('%spart %s' % (' ' * indent, n))
    #         # print('%s--------------------' % (' ' * indent))
    #         print_info(email_info, part, di, indent + 1)
    # else:
    #     content_type = msg.get_content_type()
    #     if content_type=='text/plain' or content_type=='text/html':
    #         content = msg.get_payload(decode=True)
    #         charset = guess_charset(msg)
    #         if charset:
    #             # 此处编码格式有可能会出错
    #             try:
    #                 content = content.decode('UTF-8', charset)
    #                 print('%sText: %s' % (' ' * indent, content + '...'))
    #             except Exception, e:
    #                 print('%sAttachment: %s' % (' ' * indent, content_type))
    #
    #     else:
    #         print('%sAttachment: %s' % (' ' * indent, content_type))
    email_info.setdefault(di, "")
    email_info[di] = email_info_tmp
    return email_info_tmp


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


def send_test163(text,files=None):
    pass

if __name__ == '__main__':
    #send_mail('llu@capvision.com','Cap15715','mytest 234');
    #send_mail('dbsender@capvision.com','1qaz@WSX','mytest 234dbsender');
    # recv_off365()
    print "fdfe7535534".find("1") == -1