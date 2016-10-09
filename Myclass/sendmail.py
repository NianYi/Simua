# -*- coding: gbk -*-
#!/usr/bin/env python

from smtplib import SMTP_SSL
from time import sleep
import email
import sys
import locale
class send_mail(object):
	def __init__(self,to_addr,subject_,content):
		fp=open('password.txt')
		from_addr = fp.readline().strip()
		password = fp.readline().strip()
		fp.close()
		try:
			sendsvr=SMTP_SSL('smtp.qq.com',465)
			sendsvr.user(from_addr)
			sendsvr.pass_(password)
			sendsvr.sendmail(from_addr+'@qq.com',to_addr,'''From: %s\r\nTo:%s\r\nSubject:%s\r\n\r\n%s\r\n'''%(from_addr,to_addr,subject_,content) )
			sendsvr.quit()
		except Exception,e:
			print e
		

