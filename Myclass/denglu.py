#-*- coding:utf-8 -*-
#!/usr/bin/env python
import os
import shutil
import Tkinter
from Myclass.RSA import rsa
import sqlite3
import ConfigParser
#-*-读取配置文件
config = ConfigParser.ConfigParser()
config.readfp(open('etc/pathcfg.ini','r'))
userdbPath = config.get("global","userdbpath")

class denglu(object):
        def __init__(self,top):
                self.top = top
		self.top.title('')
                #self.top.geometry('320x280+400+200')
                self.top.resizable(width=False, height=False)
		self.label = Tkinter.Label(self.top,text='Simua',font='Helvetica -50 bold')
		self.buildWidget()
		self.entryUpdate()
		Tkinter.mainloop()

	def buildWidget(self):
		self.TextInputWidth=22
                self.user = Tkinter.StringVar()
                self.passtmp = Tkinter.StringVar()
		self.password = ''
                self.userentry = Tkinter.Entry(self.top,width=self.TextInputWidth,textvariable=self.user)
                self.userentry.bind('<Return>',self.go)
		
		#-*- 密码输入框-*-
		self.passentry = Tkinter.Entry(self.top,width=self.TextInputWidth,textvariable=self.passtmp)
                self.passtmp.trace('w',self.passShow)
		self.passentry.bind('<Return>',self.go)
                #-*---------------*-
		#-*- 附加选项-*-
		
		self.is_rememberpassword = Tkinter.StringVar()
		self.is_autoload = Tkinter.StringVar()
		self.rememberpassword = Tkinter.Checkbutton(self.top,variable=self.is_rememberpassword,text='记住密码')
		self.is_rememberpassword.set(1)
		self.autoload = Tkinter.Checkbutton(self.top,variable=self.is_autoload,text='自动登录')
		self.is_autoload.set(1)
		self.label.grid()
		self.userentry.grid()
		self.passentry.grid()
		self.rememberpassword.grid(sticky=Tkinter.W)
		self.autoload.grid(sticky=Tkinter.W)

	def entryUpdate(self):
		conn = sqlite3.connect(userdbPath+'shadow.db')
		cursor = conn.cursor()
		cursor.execute("select name from sqlite_master where name='current_user'")
		relt=cursor.fetchall()
		if len(relt) != 0:
			cursor.execute("select * from current_user")
			relt = cursor.fetchall()[0]
			self.user.set(relt[0])
			if int(relt[2]) is 1:
				self.passtmp.set(rsa.decrypt(relt[1]))
			
	def passShow(self,name,index,mode):
		text_input = self.passtmp.get()
		if len(self.password)<len(text_input):
			self.password = self.password + text_input[len(self.password):]
		else:
			self.password = self.password[:len(text_input)]
		self.passtmp.set('*'*len(text_input))
		
        def go(self,env=None):
                if self.user.get()=='' or self.password=='':
                        print 'empty! try again!'
                        return
		sec = rsa()
		conn = sqlite3.connect(userdbPath+'shadow.db')
		cursor = conn.cursor()
		cursor.execute("create table if not exists user (id varchar(20) primary key, password varchar(200))")
		cursor.execute("create table if not exists current_user (id varchar(20) primary key, password varchar(200), is_remember char(1))")
		
		#-*- 将新用户插入表user中
		user_ = str(self.user.get())
		if self.is_rememberpassword.get() is True:
			password_ = rsa.encrypt(self.password)
		else:
			password_ = ''
		if self.is_userUpdate(cursor,user_) is True: 
			cursor.execute("insert into user (id,password) values (?,?)",(user_, password_))
		
		#-*- 将登录用户插入到表current_user中
		if password_ is '':
			password_ = rsa.encrypt(self.password)
		cursor.execute("delete from current_user")
		cursor.execute("insert into current_user (id,password,is_remember) values (?,?,?)",(user_, password_,str(self.is_rememberpassword.get())))
		cursor.close()
		conn.commit()
		conn.close()
		self.label.grid_forget()
		self.userentry.grid_forget()
		self.passentry.grid_forget()
		self.rememberpassword.grid_forget()
		self.autoload.grid_forget()
		self.top.quit()
	def is_userUpdate(self,cursor,user):
		cursor.execute("select * from user where id=?",(user,))
		relt = cursor.fetchall()
		if len(relt) is 0 or relt[0][1] is '':
			return True
		else:
			return False
		
