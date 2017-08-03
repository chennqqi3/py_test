#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
import time
import email
import poplib
import imaplib
import cStringIO
from hashlib import md5
from email.header import decode_header
from email.utils import parseaddr
from sqlalchemy import create_engine
from datetime import datetime
import time

reload(sys)
sys.setdefaultencoding("utf-8")

# Configuration
# -------------

# Email address
MAILADDR = "mailtondb@capvision.com"

# Email password
PASSWORD = "1qaz@WSX"

# Mail Server (pop/imap)
SERVER = "partner.outlook.cn"

# Transfer protocol (pop3/imap4)
PROTOCOL = "pop3"

# Use SSL? (True/False)
USE_SSL = True

# Main output direcotory
OUTDIR = "/home/mailbox"


def pop3(host, port, usr, pwd, use_ssl):
    """Pop3 handler

    :param host: host
    :param port: port
    :param usr: username
    :param pwd: password
    :param use_ssl: True if use SSL else False
    """
    # Connect to mail server
    try:
        conn = poplib.POP3_SSL(host, port) if use_ssl else poplib.POP3(host, port)
        conn.user(usr)
        conn.pass_(pwd)
        print("[+] Connect to {0}:{1} successfully".format(host, port))
    except BaseException as e:
        print e

    # Get email message number
    try:
        msg_num = len(conn.list()[1])
        print("[*] {0} emails found in {1}".format(msg_num, usr))
    except BaseException as e:
        print e

    conn.quit()

if __name__ == '__main__':
    pop3(SERVER, 995, MAILADDR, PASSWORD, PROTOCOL)

