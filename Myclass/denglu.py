#-*- coding:utf-8 -*-
#!/usr/bin/env python
import os
import shutil
import Tkinter
class denglu(object):
        def __init__(self,top):
                self.top = top
		self.top.title('用户代理')
                #self.top.geometry('320x280+400+200')
                self.top.resizable(width=False, height=False)
                self.label = Tkinter.Label(self.top,text='Simua',font='Helvetica -50 bold')
                self.label.grid(columnspan=2,sticky=Tkinter.N+Tkinter.S+Tkinter.W+Tkinter.E)

                self.TextInputWidth=22
		Tkinter.Label(self.top,text='用户名:').grid(sticky=Tkinter.W)
		Tkinter.Label(self.top,text='密码:').grid(sticky=Tkinter.W)
                self.user = Tkinter.StringVar()
                self.password = Tkinter.StringVar()
                self.entry = Tkinter.Entry(self.top,width=self.TextInputWidth,textvariable=self.user)
                self.entry.bind('<Return>',self.go)
                self.entry.grid(row=1,column=1,sticky=Tkinter.E)

                self.passlabel = Tkinter.Label(self.top,text='Pass')
                self.passentry = Tkinter.Entry(self.top,width=self.TextInputWidth,textvariable=self.password)
                self.passentry.bind('<Return>',self.go)
                self.passentry.grid(row=2,column=1,sticky=Tkinter.E)
                self.enter = Tkinter.Button(self.top,text='Enter',font='Helvetica 12 bold',command=self.go,activeforeground='white',activebackground='red')
                self.enter.grid(columnspan=2,sticky=Tkinter.E)
                Tkinter.mainloop()

        def go(self,env=None):
                if self.user.get()=='' or self.password.get()=='':
                        print 'empty! try again!'
                        return

                fp = open('password.txt','w')
		fp.write(str(self.user.get()) + '\n' + str(self.password.get()))
		fp.close()
		self.label.grid_forget()
		self.entry.grid_forget()
		self.passentry.grid_forget()
		self.enter.grid_forget()
		self.top.quit()
