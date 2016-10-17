#coding:utf-8
#coding:gbk
#!/usr/bin/env python
import Tkinter
from poplib import*
from  email import *
from email.utils import parseaddr
from email.header import decode_header
from email.parser import Parser
from Myclass.RSA import rsa
from django.utils.encoding import smart_str
import sqlite3
class load(object):
	from_list = []
	to_list = []
	subject_list = []
	content_list = []
	def __init__(self):
		#fp = open('password.txt')
                #username=fp.readline().strip()
                #password=fp.readline().strip()
		#password = rsa.decrypt(password)
		conn = sqlite3.connect('usr/userdb/shadow.db')
		cursor = conn.cursor()
		cursor.execute('select * from current_user')
		relt = cursor.fetchall()[0]
		username = relt[0]
		password = rsa.decrypt(relt[1])
		host = 'pop.qq.com'
		server =  POP3_SSL(host)
		try:
			server.user(username)
			server.pass_(password)
			
			rsp,mails,octets = server.list()
			for index in range(len(mails)-10,len(mails)-1):
				rsp,lines,octets = server.retr(index)
				msg_content = '\r\n'.join(lines)
				msg = Parser().parsestr(msg_content)
				self.content = ''
				#print 'first!'
				self.print_info(msg)
				load.content_list.insert(0,self.content)
				#ind=1
				#with open('oridata'+str(ind),'w') as fp:
				#	fp.write(self.content)
				#	ind+=1
		except Exception,e:
			print e
		finally:
			server.quit()
	def print_info(self,msg,indent=0):
		if indent == 0:
			for header in['From','To','Subject']:
				value  =msg.get(header,'')
	
				if value:
					if header == 'Subject':
						value = self.decode_str(value)
					else:
						hdr,addr = parseaddr(value)
						name = self.decode_str(hdr)
						value = '%s <%s>' % (smart_str(name), smart_str(addr))
					if header == 'From':
						load.from_list.insert(0,value)
					elif header == 'To':
						load.to_list.insert(0,value)
					else:
						load.subject_list.insert(0,value)
		if (msg.is_multipart()):
			parts = msg.get_payload()
			for n, part in enumerate(parts):
				#print('%spart %s' % ('  ' * indent, n))
				#print('%s--------------------' % ('  ' * indent))
				#self.content = self.content+'%s--------------------' % ('  ' * indent)
				self.print_info(part, indent + 1)
		else:
			content_type = msg.get_content_type()
			if content_type=='text/plain' or content_type=='text/html':
				content = msg.get_payload(decode=True)
			#	with open('oridata1','w') as fp:
			#		fp.write(content)
			#	print content
			#	charset = self.guess_charset(msg)
			#	if charset:
			#		try:
			#			content = content.decode(charset)
			#		except:
			#			print 'content_code_eoor'
			#			pass
				self.content = self.content + '%s%s\n' % ('  ' * indent, content)
				#print	content
			else:
				self.content = self.content + '%sAttachment: %s\n' % ('  ' * indent, content_type)
				#print('%sAttachment: %s' % ('  ' * indent, content_type))
	def decode_str(self,s):
		value, charset = decode_header(s)[0]
		if charset:
			#print charset
			try:
				value = value.decode(charset)
			except:
				#print 'decode_str_eooor'
				value=smart_str(value)
				#print len(value)

		return value
	def guess_charset(self,msg):
		charset = msg.get_charset()
		if charset is None:
			content_type = msg.get('Content-Type', '').lower()
			pos = content_type.find('charset=')
			if pos >= 0:
				charset = content_type[pos + 8:].split(';')[0]
		return charset.strip()

