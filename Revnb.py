import requests, urllib3, re, time, random, sys, os, socket
from colorama import Fore, Back, Style, init
from multiprocessing.dummy import Pool

init()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

thread = 100
tmpSites = []; ipsList = []
outputFile = open("sr_sites.txt", "a")

def logo():
    colors = list(vars(Fore).values())
    os.system(["clear", "cls"][os.name == 'nt'])
    Logo = '''
        ______  __      ____            ____
       / ___/ |/ /     / __ \___ _   __/  _/___
       \__ \|   /_____/ /_/ / _ \ | / // // __ \\
      ___/ /   /_____/ _, _/  __/ |/ // // /_/ /
     /____/_/|_|    /_/ |_|\___/|___/___/ .___/
     {y}Finix {w}[{g}@{w}] {y}Zonexploiter          /_/ {w}v3\n\n'''.format(g=Fore.GREEN, w=Fore.WHITE, m=Fore.MAGENTA, y=Fore.YELLOW, r=Fore.RED)
    for line in Logo.splitlines():
        print("".join(colors[random.randint(1, len(colors)-1)] + line.format(w=Fore.WHITE, r=Fore.RED)))
        time.sleep(0.05)

def opt():
    siteList = []
    fileName = raw_input(" {w}[{g}+{w}] {y}the list {w}> ".format(w=Fore.WHITE, g=Fore.GREEN, y=Fore.YELLOW))
    if os.path.exists(fileName): siteList = open(fileName, "r+").readlines()
    else:
        print(" {A}[{B}x{A}] {B}The list not found in current dir".format(A=Fore.WHITE, B=Fore.BLUE))
        exit()
    theThread = raw_input(" {w}[{g}+{w}] {y}thread {w}({y}default{w}:{y}100{w}) {w}> ".format(w=Fore.WHITE, g=Fore.GREEN, y=Fore.YELLOW))
    if theThread == "": theThread = 100
    if siteList == []:
        print(" {A}[{B}x{A}] {B}Empty list".format(A=Fore.WHITE, B=Fore.BLUE))
        exit()
    else:
        if len(siteList) < int(theThread): theThread = len(siteList)
        return siteList, int(theThread)

class ReverseIp:

    def __init__ (self, ip):
        self.headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0' }
        self.result = [];
        self.ip = ip

    def filter ( self, site ):
        global tmpSites
        site = site.replace("www.", "").replace('cpanel.', '').replace('autodiscover.', '').replace('webmail.', '').replace('webdisk.', '').replace('ftp.', '').replace('cpcalendars.', '').replace('cpcontacts.', '').replace('mail.', '').replace('ns1.', '').replace('ns2.', '').replace('smtp.', '')
        if site != "" and site not in self.result and site not in tmpSites: 
            tmpSites.append(site)
            self.result.append(site)
        return 0

    def sonar ( self ):
        try:
            response = requests.get( "https://sonar.omnisint.io/reverse/" + self.ip, headers = self.headers )
            for site in response.json(): self.filter( site )
            return 1
        except: return 0

    def execute (self):
        global outputFile, tmpSites

        self.sonar()
        if len( self.result ) != 0:
            outputFile.write("\n".join(self.result))
            return len(self.result)
        else: return 0

def perror (url, msg): print(Back.RED+" -- "+msg+" -- \033[0m "+url)
def psucces (url, count): print(Back.GREEN + Fore.WHITE + " -- "+str(count)+" SITES -- \033[0m "+url)

def rev(url):
    global tmpSites, outputFile, ipsList
    if url.startswith("http://"): url = url.replace("http://", "")
    elif url.startswith("https://"): url = url.replace("https://", "")
    url = url.replace("\n", "").replace("\r", "").replace("/", "")
    try:
        ip = socket.gethostbyname(url)
        if ip in ipsList: print(Back.RED+" -- SAME IP -- \033[0m "+url); return 0
        ipsList.append(ip)
        revip = ReverseIp(ip)
        result = revip.execute()
        if result <= 0: perror(url, "EMPTY")
        else: psucces(url, result)
    except Exception as e: perror(url, "ERROR")

if __name__ == "__main__":
    try:
        logo(); sx = opt(); print("\n")
        pool = Pool(sx[1])
        pool.map(rev, sx[0])
        pool.close()
        pool.join()
        print("\n {A}[{B}+{A}] {Y}Done {A}: {Y}{S} sites".format(Y=Fore.YELLOW,A=Fore.WHITE, B=Fore.BLUE, S=(str(len(tmpSites)))))
    except KeyboardInterrupt:
        print("\n {w}[{r}-{w}] {b}Goodbye >//< ".format(w=Fore.WHITE, r=Fore.RED, b=Fore.BLUE))
