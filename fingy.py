import logging
import platform
import socket
import subprocess
import sys
from datetime import datetime as date
from logging.handlers import RotatingFileHandler
from os import path, remove, system
from time import sleep

import colorama
import getmac

import passwd
import scanmodule
import utils

colorama.init()
#Setting up log
log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatt = logging.Formatter("|%(asctime)s:  %(levelname)s - %(message)s")
fileh = RotatingFileHandler('fingy.log', 'w+', 1000000, 5)
fileh.setLevel(logging.DEBUG)
fileh.setFormatter(formatt)
log.addHandler(fileh)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARN)
log.addHandler(stream_handler)
log.info("NEW EXECUTION")
#Starting...
print(colorama.Fore.BLUE+"""
        ███████╗██╗███╗   ██╗ ██████╗██╗   ██╗
        ██╔════╝██║████╗  ██║██╔════╝╚██╗ ██╔╝
        █████╗  ██║██╔██╗ ██║██║  ███╗╚████╔╝ 
        ██╔══╝  ██║██║╚██╗██║██║   ██║ ╚██╔╝  
        ██║     ██║██║ ╚████║╚██████╔╝  ██║   
        ╚═╝     ╚═╝╚═╝  ╚═══╝ ╚═════╝   ╚═╝    
                {0}
    """.format(colorama.Fore.WHITE+colorama.Style.BRIGHT+"Version:  Not really stable"+colorama.Style.RESET_ALL))
if not utils.Main().mycostatus:
    log.critical("You're not connected to Internet")
    sys.exit()
else:
    utils.Main().MyPcDetails()
if len(sys.argv) >= 2:
    if len(sys.argv) == 3:
        if sys.argv[2] == "--entire" or sys.argv[2] == "-e":
            scanentirenetwork = True
        else:
            scanentirenetwork = False
    else:
        scanentirenetwork = False
    try:
        x = int(sys.argv[1].split("-")[0])
        y = int(sys.argv[1].split("-")[1])
    except:
        log.warning("Usage: 'reload 1-256 (-e: scan the entire network)'")
        x = 1
        y = 2
else:
    scanentirenetwork = False
    x = 1
    y = 26
try:
    remove("__pycache__")
except (PermissionError,FileNotFoundError) as e:
    log.info(e)
try:
    from webbrowser import open_new_tab
    webbrowser = True
except ModuleNotFoundError:
    log.warn("Webbrowser module not found, but anyway ;)")
    webbrowser = False

vendors = {}
def retreive_vendors():
    try:
        a=open("mac_vendors.txt",encoding="utf-8").read()
    except FileNotFoundError:
        return False
    for i in a.split("\n"):
        identifier = i[0:6]
        vendor = i.split(identifier)[1].strip()
        if "#" in vendor:
            if vendor.startswith("W-Ie-"):
                vendor = vendor.split("#")[0].strip()
            elif "-" in vendor:
                vendor = vendor.split("-")[0]
            elif "+" in vendor:
                vendor =vendor.split("+")[0]
            elif "&" in vendor:
                vendor =vendor.split("&")[0]
            else:
                vendor = vendor.split("#")[0].strip()
        if vendor[-1] == "/":
            vendor = vendor[:-1]
        vendors[identifier] = vendor
retreive_vendors()
def SortIp(ips:list):
    last_bits=[]
    three_first_bits = ".".join(ips[0].split(".")[0:-1])+"."
    sorted_ips = []
    for i in ips:
        last_bit=i.split(".")[-1]
        last_bits.append(last_bit)
    sorted_ips.sort(key=int)
    for i in last_bits:
        sorted_ips.append(three_first_bits+i)
    return sorted_ips
log.info(dir())
utils.Addpid()
ipndhstname = {}
ipndports = {}
ups = []
socket.setdefaulttimeout(0.05)
local_ip = passwd.GetLocalIp()
log.info("Hosts discovery processus started")
if scanentirenetwork:
    scan_choice = scanmodule.Pingy().EntireNetwork(x,y)
else:
    sfff = scanmodule.Pingy().improvedscan()
    scan_duration = sfff[1]
    scan_choice = sfff[0]
for fghm in scan_choice:
    ups.append(fghm)
log.info(ups)
if len(ups) <= 2:
    log.warning(scanmodule.Pingy().warning)
    log.info("Typing 'up' is advisable")
for xa in ups:
    try:
        hst,tm,pt = socket.gethostbyaddr(str(xa))
    except (socket.herror, socket.gaierror):
        try:
            hst,tm,pt = socket.gethostbyaddr(str(xa))
        except (socket.herror, socket.gaierror):
            hst = 'Unknown'
    ipndhstname[xa] = hst
if utils.Main().mycostatus == False:
    log.warning("No Internet")

myplatform = platform.system().lower()
if myplatform == 'windows':
    clear = "cls"
else:
    clear = "clear"
print("+..............................+")
print(colorama.Style.BRIGHT+"{0} {1} {2}".format(colorama.Fore.GREEN+"[+]",colorama.Fore.WHITE+str(len(ups)),colorama.Fore.WHITE+"device(s) found"))
print("Finished at",str(date.now())[11:-7])
print("+..............................+")
print(colorama.Style.RESET_ALL)
while True:
    try:
        menu = input("$> ")
    except KeyboardInterrupt:
        print(colorama.Back.LIGHTMAGENTA_EX+"Use exit to quit")
        print(colorama.Style.RESET_ALL)
    except EOFError:
        log.warning("Stop messing around with it")
        continue
    log.info("INPUT-> "+menu)
    if menu == 'help' or menu == 'h':
        print(colorama.Style.RESET_ALL+"|------------HELP------------|")
        print("")

        print(colorama.Fore.WHITE+colorama.Style.BRIGHT+"a- Scan results")
        print(colorama.Style.RESET_ALL+"1- Get ip details")
        print(" - reload [+args]")
        print(" - {}".format(colorama.Fore.WHITE+colorama.Style.BRIGHT+"update"))
        print(colorama.Style.RESET_ALL+" - ls")
        print(" - exit")
        print("|----------------------------|")
        continue
    if menu == "up -h" or menu == "update -h" or menu == "up --help" or menu == "update --help":
        print("Use 'update' or 'up' to refresh the devices found list")
        print("It DOES NOT reload the script unlike 'reload'")
    if menu == "up" or menu == "update":
        if utils.Main().mycostatus == False:
            log.warning("No Internet")
        del ups
        del ipndhstname
        ups = []
        ipndhstname = {}
        ups.clear()
        for fghm in scanmodule.Pingy().improvedscan()[0]:
            ups.append(fghm)
        ups = SortIp(list(set(ups)))
        for xl in ups:
            try:
                hst,tm,pt = socket.gethostbyaddr(str(xl))
            except (socket.herror, socket.gaierror):
                try:
                    hst,tm,pt = socket.gethostbyaddr(str(xl))
                except (socket.herror, socket.gaierror):
                    hst = 'Unknown'
            ipndhstname[xl] = hst
        deb = colorama.Fore.WHITE+"{} device(s) found".format(str(len(ups)))
        print(colorama.Style.BRIGHT+"{0} ".format(colorama.Fore.GREEN+"[+]")+deb)
        log.info(ups)
    if menu == "h(r)" or menu == "help(r)" or menu == "help(reload)" or menu == "reload -h" or menu == "reload --help":
        print("|-----------------------------HELP(RELOAD)-----------------------------|")
        print("Type 'reload' to reload the script")
        print("This command supports a few arguments:")
        print("     r(eload) -h (or --help)")
        print("     reload 1-25 : restart by scanning your network from 192.168.1.1 to 25")
        print("     reload 1-25 --sudo : try to run as root")
        print("     reload (+args) -e : restart by scanning the entire network")
    if menu == "reload" or menu == "r":
        if utils.Main().mycostatus == False:
            log.error("No Internet->Unable to reload")
            continue
        try:
            subprocess.Popen([sys.executable, path.realpath(__file__)])
        except KeyboardInterrupt:
            pass
        except Exception as e:
            log.error(exc_info=1)
            continue
        
    if "reload " in menu and not "-h" in menu and not "--help" in menu:
        if utils.Main().mycostatus == False:
            log.error("No Internet->Unable to reload")
            continue
        try:
            arggs = menu.split()[1]
        except IndexError:
            print("J'ai pas tout suivi, recommence stp")
            continue
        try:
            argz = menu.split()[2]
        except IndexError:
            continue
        try:
            if menu.split()[2] == "--sudo":
                try:
                    if myplatform != "windows":
                        subprocess.Popen(["sudo",sys.executable, path.realpath(__file__),arggs])
                except:
                    log.critical("Unable to reload the script as admin")
                    continue
            elif "-e" in menu.split() or "--entire" in menu.split():
                subprocess.Popen([sys.executable,path.realpath(__file__),arggs,"-e"])
        except IndexError:
            try:
                subprocess.Popen([sys.executable, path.realpath(__file__),arggs])
            except:
                log.critical("Failed to reload",exc_info=1)
                continue
        
    
    if menu == 'exit':

        try:
            puids = open("puids.txt","r")
            for puidss in puids.readlines():
                if myplatform == "windows":
                    taskkill = subprocess.Popen(['taskkill','/F','/PID','{}'.format(int(puidss[:-1]))], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                else:
                    taskkill = subprocess.Popen(['kill','{}'.format(int(puidss[:-1]))], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            puids.close()
        except Exception as e:
            log.error(e)
        remtmp = remove("puids.txt")
        remtmp = open("puids.txt","a").close()
        sys.exit(0)

    if menu == '1':
        try:
            instance_testmyco_module = utils.Main()
            entree_pour_details = input("Ip=> ")
            if scanmodule.IsValidIp(entree_pour_details) == True or scanmodule.IsValidIp(entree_pour_details) == False:
                instance_testmyco_module.IpDetails(entree_pour_details)
            else:
                print("Unable to reach {0}".format(entree_pour_details))
        except Exception as e:
            log.error("Getting details for "+entree_pour_details+" failed",exc_info=1)
            continue

    if menu == 'a':
        if len(ups) == 0:
            print("No host found")
            continue
        ups=SortIp(ups)
        log.info(ups)
        print(colorama.Fore.YELLOW+"+----------------------------------------------------------------------------------------------------------------------------------------------+"+colorama.Style.RESET_ALL)
        port = ['20','21','22','23','25','37','43','53','69','80','111','135','137','138','139','443','445','548','631','989','993','995','990','2049','4444','4443','8080','8081','49152','62078','49674','49664','49665','49666','49666','49861','49862']
        for g in range(len(ups)):
            print(colorama.Style.RESET_ALL+colorama.Fore.GREEN+"(+)"+" {}".format(colorama.Fore.WHITE+ups[g]))
            ports_found = []
            for d in port:
                soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                result = soc.connect_ex((str(ups[g]),int(d)))
                soc.close()
                try:
                    utilisationduport = socket.getservbyport(int(d))
                    if result == 0:
                        ports_found.append("{0}:{1}/tcp".format(str(d),utilisationduport))
                except OSError:
                    pass
                ipndports[str(ups[g])] = ports_found
        def get_vendor(mac):
            if mac == None:
                return "Unknown"
            id = [i.upper() for i in "".join(mac.split(":")[:3]).split()][0]
            if id in vendors.keys():
                vendor = vendors[id]
            else:
                vendor = "Unknown"
            return vendor
        print(colorama.Fore.YELLOW+"|-------IP------|--------Hostname--------|--------------Ports---------------|---------MAC---------|--------------VENDOR------------")
        for pres in ups:
            print("|",colorama.Style.BRIGHT+"{}".format(colorama.Fore.YELLOW+pres))
            print(colorama.Style.NORMAL+"|                ",colorama.Fore.YELLOW+ipndhstname[pres])
            for mmlkj in ipndports[pres]:
                print("|                                          ",mmlkj)
            mac = getmac.get_mac_address(ip=pres)
            print("|                                                                            ",mac)
            print("|                                                                                                   ",get_vendor(mac))
        print("+----------------------------------------------------------------------------------------------------------------------------------------------+"+colorama.Style.RESET_ALL)
        continue
