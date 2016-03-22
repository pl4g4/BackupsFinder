#!/usr/bin/python

import requests, os, sys, argparse, pycurl, urllib
from colorama import Fore, Back, Style, init
from io import BytesIO
init(autoreset=True)

parser = argparse.ArgumentParser(prog='BackupsFinder', description='Find directories')
parser.add_argument("--url", help="URL", type=str, required=True, metavar='The URL')
parser.add_argument("--proxy", help="Set proxy", type=str, metavar='Proxy')
parser.add_argument("--useragent", help="Set User Agent", type=str, metavar='User Agent', default='Firefox')
parser.add_argument("--dic", help="The path where the txt file is located", type=str, default='backupsdir.txt', metavar='File Path')
args = parser.parse_args()

def readFile(filePath):
	CURSOR_UP_ONE = '\x1b[1A'
	ERASE_LINE = '\x1b[2K'
	if os.path.exists(filePath):
		with open(filePath, 'r') as item:
			try:
				for line in item:					

					lineSplitted = line.split('/', 10 )		
					newString = ''

					for i in lineSplitted:
						newString += '/'+urllib.quote_plus(i.rstrip('\n'))

					url = args.url+newString

					try:

						buffer = BytesIO()

						c = pycurl.Curl()
						c.setopt(c.URL, url)
						c.setopt(c.WRITEFUNCTION, buffer.write)
						c.setopt(c.CONNECTTIMEOUT, 5)
						c.setopt(c.FOLLOWLOCATION, True)
						c.setopt(c.TIMEOUT, 3)
						c.setopt(c.USERAGENT, args.useragent)

						if args.proxy:
							c.setopt(c.PROXY, args.proxy)

						c.perform()	

						body = buffer.getvalue()
						find = 'Index of'
						code = c.getinfo(c.RESPONSE_CODE)

						foundString =  body.find(find)	

						if code == 200 and foundString > 0:
							print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
							print( Fore.GREEN + "FOUND -  Status Code: " + str(code) + ' --- Path: '+ url + '\n\n' )
						else:						
							print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
							print("Checking - Status Code: " + str(code) + " Path: "+ line ),
					except Exception as e:
						print e
													
			except Exception as e:
				print e

			print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
	else:
		print "File not Found"

def main(args):

	if (len(sys.argv) < 2) | (len(sys.argv) > 8):
		sys.exit('Invalid number of parameters, use -h for help')

	print("===================================================================================================")
	print("                 	    Finding possible paths in "+args.url+"                                    ")
	print("===================================================================================================")
	print('')
	readFile(args.dic)
	print("===================================================================================================")

if __name__ == '__main__':
	main(args)
	sys.exit()
