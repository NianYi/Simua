#-*- coding:utf-8 -*-
#!/usr/bin/env python
import os
import shutil
import Tkinter
from Myclass.RSA import rsa
class denglu(object):
        def __init__(self,top):
                self.top = top
		self.top.title('用户代理')
                #self.top.geometry('320x280+400+200')
                self.top.resizable(width=False, height=False)
                self.label = Tkinter.Label(self.top,text='Simua',font='Helvetica -50 bold')
                self.label.grid(columnspan=2,sticky=Tkinter.N+Tkinter.S+Tkinter.W+Tkinter.E)

                self.TextInputWidth=22
		self.userLabel=Tkinter.Label(self.top,text='用户名:')
		self.userLabel.grid(sticky=Tkinter.W)
		self.passLabel=Tkinter.Label(self.top,text='密码:')
		self.passLabel.grid(sticky=Tkinter.W)
                self.user = Tkinter.StringVar()
                self.passtmp = Tkinter.StringVar()
		self.password = ''
                self.userentry = Tkinter.Entry(self.top,width=self.TextInputWidth,textvariable=self.user)
                self.userentry.bind('<Return>',self.go)
                self.userentry.grid(row=1,column=1,sticky=Tkinter.E)
		
		#-*- 密码输入框-*-
		self.passentry = Tkinter.Entry(self.top,width=self.TextInputWidth,textvariable=self.passtmp)
                self.passtmp.trace('w',self.passShow)

		self.passentry.bind('<Return>',self.go)
                self.passentry.grid(row=2,column=1,sticky=Tkinter.E)
                #-*---------------*-
		

		self.enter = Tkinter.Button(self.top,text='Enter',font='Helvetica 12 bold',command=self.go,activeforeground='white',activebackground='red')
                self.enter.grid(columnspan=2,sticky=Tkinter.E)
                Tkinter.mainloop()
	def passShow(self,name,index,mode):
		text_input = self.passtmp.get()
		print '*号---',text_input
		if len(self.password)<len(text_input):
			self.password = self.password + text_input[len(self.password):]
		else:
			self.password = self.password[:len(text_input)]
		print 'pass---',self.password
		#if len(self.passtmp.get()) == 0:
		#	self.password = ''
		self.passtmp.set('*'*len(text_input))
		
        def go(self,env=None):
                if self.user.get()=='' or self.password=='':
                        print 'empty! try again!'
                        return
		sec = rsa()
		fp = open('password.txt','w')
		fp.write(str(self.user.get()) + '\n' + rsa.encrypt(self.password))
		fp.close()
		self.label.grid_forget()
		self.userentry.grid_forget()
		self.passentry.grid_forget()
		self.enter.grid_forget()
		self.userLabel.grid_forget()
		self.passLabel.grid_forget()
		self.top.quit()
