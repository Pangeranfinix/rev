#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author imamwawe
import os
import re
import random
import base64
import requests
from colorama import *
import concurrent.futures
init(autoreset=True);R = Fore.LIGHTRED_EX;G = Fore.LIGHTGREEN_EX;C = Fore.LIGHTCYAN_EX;W = Fore.LIGHTWHITE_EX;reset = Fore.RESET
requests.urllib3.disable_warnings()
class Subdomains:
	def __init__(self):
		self.ress = 0
		self.loop = 0
	def logo(self):
		os.system("cls" if os.name == "nt" else "clear")
		print (f"""{C}
___       ___________       ___________
__ |     / /__    |_ |     / /__  ____/  {W}SCAN{C}
__ | /| / /__  /| |_ | /| / /__  __/     {W}SUBDOMAINS{C}
__ |/ |/ / _  ___ |_ |/ |/ / _  /___     {W}V1.0{C}
____/|__/  /_/  |_|___/|__/  /_____/     {W}By t.me/Imamwawe
		""")
	def api(self, target):
		try:
			self.loop += 1
			target = re.findall(r"(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}", target)[0]
			api = requests.get(f"https://sonar.omnisint.io/subdomains/{target}", headers={"user-agent":"Mozilla/5.0 (Linux; Android 10; M2004J19C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36"}, stream=True, verify=False, timeout=30).json()
			with open("subdomains.txt", "a+") as output:
				for results in api:
					if results != "error":
						self.ress += 1
						output.write(f"{results}\n")
		except:pass
		print (f"\r[ SCAN SUBDOMAINS ] {self.loop}/{self.all} results: {self.ress}", end="")
	def main(self):
		self.logo()
		while True:
			try:
				file = open(input("[*] Input file : "), errors="ignore").read().splitlines()
				self.all = len(file)
				break
			except FileNotFoundError:
				print (f"[{R}!{W}] File not found")
				continue
		thread = int(input("[*] Input thread : "))
		with concurrent.futures.ThreadPoolExecutor(max_workers=thread) as th:
			[th.submit(self.api, target) for target in file]
if __name__=="__main__":
	Subdomains().main()