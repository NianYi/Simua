#-*- coding:utf-8 -*-
#!/usr/bin/env python
import Tkinter
import ttk
from bs4 import BeautifulSoup as BS
from Myclass.download import load
from Myclass.sendmail import send_mail
from time import sleep
import thread
class Show(object):
	cur_page=1
	def __init__(self,root):
		self.numofperpage = 6
		self.pagenum = 0
		self.index = 0
		self.messnum = 0
	
		self.root = root
		self.root.title('Simua')
                self.root.geometry('1100x600+100+100')
		self.root.resizable(width=False, height=False)
		style = ttk.Style(self.root)
		style.configure('TButton',font='Helvetica -14 bold',width=18)

		self.maincolor = 'white'
		self.top = Tkinter.Frame(self.root,background=self.maincolor)
		self.top.pack(fill=Tkinter.X,side=Tkinter.TOP)
		self.lastpage = ttk.Button(self.top,text='<-',command=lambda x=0:self.switch_page(x))
		self.nextpage = ttk.Button(self.top,text='->',command=lambda x=1:self.switch_page(x))
		self.subject_label = ttk.Label(self.top,text=' '*30+'Subject',font='Helvetica -18 ')

		self.send=ttk.Button(self.top,text='send',command=self.send_message)
		self.fresh=ttk.Button(self.top,text='fresh')
		self.lastpage.pack(side=Tkinter.LEFT)
		self.nextpage.pack(side=Tkinter.LEFT)
		self.subject_label.pack(side=Tkinter.LEFT,fill=Tkinter.BOTH,expand=True)
		self.send.pack(side=Tkinter.RIGHT)
		self.fresh.pack(side=Tkinter.RIGHT)
	
		self.middle = Tkinter.Frame(self.root,background='white')
		self.middle.pack(fill=Tkinter.X,side=Tkinter.TOP)
		self.title_list = []
		self.var_list = []
		#style = ttk.Style(self.root)
		#style.configure('TButton',font='Helvetica -14 bold',width=18)
		for ind in range(0,self.numofperpage):
			var = Tkinter.StringVar()
			title = ttk.Button(self.middle,command=lambda x=ind: self.click(x),textvariable=var,style='TButton')
			self.title_list.append(title)
			self.var_list.append(var)
#-*- 刷新标题-*-
		#self.title_update()
		
		self.bottom = Tkinter.Frame(self.root,background='green')
		self.conscrl = Tkinter.Scrollbar(self.bottom)
		self.content = Tkinter.Text(self.bottom,font='Helvetica -15 ',yscrollcommand=self.conscrl.set)
#		self.conscrl.pack(fill=Tkinter.Y,side=Tkinter.RIGHT)
		self.conscrl['command'] = self.content.yview
		self.content.pack(fill=Tkinter.BOTH,expand=True,side=Tkinter.LEFT)
		self.bottom.pack(fill=Tkinter.BOTH,expand=True,side=Tkinter.TOP)
#-*-刷新内容-*-		
		#self.content_update()
		thread.start_new_thread(self.jobctl,())
		self.root.mainloop()
	
	def jobctl(self):
		msg = load()
		self.messnum = len(load.from_list)
		self.title_update()
		self.content_update()

	def title_update(self):
		self.pagenum = (self.messnum+self.numofperpage-1)/self.numofperpage
		end=self.numofperpage
		if Show.cur_page == self.pagenum:
			end=self.messnum-(Show.cur_page-1)*self.numofperpage
		
		for ind in range(0,end):
			#self.var_list[ind].set("ni\nfddf")
			subject_ = load.subject_list[ind+self.numofperpage*(Show.cur_page-1)]
			subject_ = subject_.replace(' ','')
			from_ = load.from_list[ind+self.numofperpage*(Show.cur_page-1)]
			from_ = from_[from_.find('<')+1:from_.find('>')]
			print subject_+'\n'+from_
			self.var_list[ind].set(subject_[0:10]+'\n'+subject_[5:14]+'..')
			self.title_list[ind].grid(row=0,column=ind)
		if end < self.numofperpage:
			for ind in range(end,self.numofperpage):
				self.title_list[ind].grid_forget()

	def content_update(self):
		self.content.delete(0.0,Tkinter.END)
		soup = BS(load.content_list[self.index+self.numofperpage*(Show.cur_page-1)],'html.parser')
        	#print soup.title.string
        	texts = soup.get_text().strip().split('\n')
		
		for i in texts:
			if i.strip() != '':
				self.content.insert(Tkinter.END,i.strip()+'\n')
		#self.conscrl.pack(fill=Tkinter.Y,side=Tkinter.RIGHT,expand=True)

	def click(self,ind):
		self.index = ind
		self.content_update()
		print ind
	def switch_page(self,flag):
		if flag == 0 and Show.cur_page > 1:
			Show.cur_page = Show.cur_page-1
			self.title_update()
			self.index = 0
			self.content_update()
		elif flag == 1 and Show.cur_page < self.pagenum:
			Show.cur_page = Show.cur_page+1
			self.title_update()
			self.index = 0
			self.content_update()
		print Show.cur_page
	def send_message(self):
		self.send_frame = Tkinter.Toplevel()
		self.send_frame.geometry('550x300+300+100')
		self.send_frame.title('写邮件')
		self.rcv_var = Tkinter.StringVar(self.send_frame)
		self.subject_var = Tkinter.StringVar(self.send_frame)
		self.content_var = Tkinter.StringVar(self.send_frame)

		rcv_frame = Tkinter.Frame(self.send_frame)
		rcv_label = Tkinter.Label(rcv_frame,text='收件人:')
		rcv_input = Tkinter.Entry(rcv_frame,textvariable=self.rcv_var)
		rcv_input.pack(fill=Tkinter.X,side=Tkinter.RIGHT,expand=True)
		rcv_label.pack(side=Tkinter.LEFT)
		rcv_frame.pack(fill=Tkinter.X,side=Tkinter.TOP)
		
		subject_frame = Tkinter.Frame(self.send_frame)
		subject_label = Tkinter.Label(subject_frame,text='主 题:')
		subject_input = Tkinter.Entry(subject_frame,textvariable=self.subject_var)
		subject_input.pack(fill=Tkinter.X,side=Tkinter.RIGHT,expand=True)
		subject_label.pack(side=Tkinter.LEFT)
		subject_frame.pack(fill=Tkinter.X,side=Tkinter.TOP)
		
		self.content_input = Tkinter.Text(self.send_frame,relief=Tkinter.FLAT,bd=0)
		self.content_input.pack(fill=Tkinter.BOTH)
		send_button = Tkinter.Button(self.send_frame,text='发送',command=self.send)
		send_button.pack(side=Tkinter.RIGHT)
		self.send_frame.mainloop()
	def send(self):
		print self.content_input.get()
	#	send = send_mail(self.rcv_var.get(),self.subject_var.get(),self.content_var.get())
	#	self.send_frame.quit()
