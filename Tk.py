#-*- coding:utf-8 -*-
#!/usr/bin/env python
import Tkinter
#from bs4 import BeautifulSoup as BS
from Myclass.denglu import denglu
from Myclass.Show import Show
from Myclass.download import load
import thread
from time import sleep,ctime
def main():
	try:
		root = Tkinter.Tk()
		dL = denglu(root)
		show = Show(root)
	except:

		exit(0)
if __name__=='__main__':
	main()
