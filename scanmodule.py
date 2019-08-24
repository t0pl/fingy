import socket
import subprocess
import threading
from ipaddress import IPv4Address, IPv6Address
from time import sleep
import datetime

import passwd

main_thread = threading.currentThread()
streds=[]
class Pingy():
    ups = []
    def __init__(self):
        self.warning = "The number of threads might not be supported by some devices so the number of devices found can be LOWER"
        self.iplocal = passwd.GetLocalIp()
        self.racine = ".".join(self.iplocal.split('.')[0:-1]) + '.'
        self.deuxpremiers = ".".join(self.iplocal.split('.')[0:2]) + '.'
        self.troisiemeoctet = int(self.iplocal.split(".")[2])
    def Pingg(self, target:str):
        _ping_ = subprocess.Popen(['ping','-4','-n','1','{}'.format(target)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sortie, erreurs = _ping_.communicate()
        if "TTL" in str(sortie) or "ttl" in str(sortie):
            return True
        else:
            return False
    def Ping(self, target:str):
        _ping_ = subprocess.Popen(['ping','-n','1','{}'.format(target)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sortie, erreur = _ping_.communicate()
        if "TTL" in str(sortie) or "ttl" in str(sortie):
            self.ups.append(target)
    def ScanAll(self, x=1,y=25,sauf=[]):
        if x > y:
            return False
        for number in range(x,y):
            if number in sauf:
                continue
            else:
                r = self.racine+str(number)
                stred = threading.Thread(target=self.Ping, args=[r,])
                stred.start()
                streds.append(stred)
                if len(threading.enumerate()) > 200:
                    for i in threading.enumerate():
                        if main_thread is i or streds[-1] is i or streds[-2] is i:
                            continue
                        i.join()
        self.ups = list(dict.fromkeys(self.ups))
        return self.ups
    def EntireNetwork(self, x_third_oct=1, y_third_oct=2558, x=1,y=26):
        streds = []
        if y_third_oct == 2558:
            y_third_oct = self.troisiemeoctet
        for lsd in range(x_third_oct,y_third_oct):
            for m in range(x,y):
                rimk = self.deuxpremiers+str(lsd)+"."+str(m)
                stred = threading.Thread(target=self.Ping, args=[rimk, ])
                stred.start()
                streds.append(stred)
                if len(threading.enumerate()) > 200:
                    for i in threading.enumerate():
                        if main_thread is i or streds[-1] is i or streds[-2] is i:
                            continue
                        i.join()
            print(self.deuxpremiers+str(lsd)+".1/{}".format(str(y-1)))
        self.ups = list(dict.fromkeys(self.ups))
        return self.ups
    def improvedscan(self):
        a=[]
        debug = {"StartingTime":datetime.datetime.now()}
        for i in range(2):
            list(set(a))
            debug["Round "+str(i)] = {"(var)a":len(a)}
            if i != 0:
                for x in self.ScanAll(x=1,y=256,sauf=[int(x.split(".")[3]) for x in a]):
                    a.append(x)
                debug["Round "+str(i)]["FinishedTime"] = datetime.datetime.now()
            else:
                for x in self.ScanAll(x=1,y=256):
                    a.append(x)
                debug["Round "+str(i)]["FinishedTime"] = datetime.datetime.now()
        debug["EndingTime"] = datetime.datetime.now()
        debug["EndminusStart"] = debug["EndingTime"] - debug["StartingTime"]
        return (list(set(a)),debug)

def IsHttpPortOpen(target:str):
    try:
        res = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        re = res.connect_ex((target,80))
    except Exception as e:
        print(e)
        return False
    finally:
        res.close()
    if re == 0:
        return True
    else:
        return False
def IsValidIp(ip):
    #return False for IPv4, True for v6, None if not valid
    ip = str(ip)
    try:
        IPv6Address(ip)
    except:
        try:
            IPv4Address(ip)
        except:
            return None
        else:
            return False
    else:
        return True
common_used_port_list = ['20','21','22','23','25','37','43','53','69','80','111','135','137','138','139','443','445','548','631','989','993','995','990','2049','4444','4443','49152','62078']
class Scan():
    hote = "_"
    open_tcp_ports = []
    closed_tcp_ports = []
    def __init__(self, hote):
        self.hote = str(hote)
        if IsValidIp(self.hote) == None:
            self.hote = '127.0.0.1'
    def TcpOpen(self, xx=False, yy=False,usage_common_used_port_list=False):
        self.open_tcp_ports = []
        self.closed_tcp_ports = []
        if self.hote != False:
            print("Target: ",self.hote)
            print("Tcp scan running...")
            if usage_common_used_port_list == True:
                for ix in common_used_port_list:
                    ix = int(ix)
                    sb = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socket.setdefaulttimeout(0.0000005)
                    ab  = sb.connect_ex((self.hote, ix))
                    sleep(0.0000005)
                    sb.close()
                    if int(ab) == 0:
                        self.open_tcp_ports.append(ix)
                self.closed_tcp_ports.append(len(common_used_port_list) - len(self.open_tcp_ports))
                return self.open_tcp_ports, self.closed_tcp_ports
            if usage_common_used_port_list == False and xx == False or yy == False:
                #With no paramaters
                xx = 80
                yy = 81
                for ix in range(xx, yy):
                    sb = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socket.setdefaulttimeout(0.0005)
                    ab  = sb.connect_ex((self.hote, ix))
                    sleep(0.0000001)
                    sb.close()
                    if int(ab) == 0:
                        self.open_tcp_ports.append(ix)
                self.closed_tcp_ports.append((max(yy, xx)-min(yy,xx))-len(self.open_tcp_ports))
                return self.open_tcp_ports, self.closed_tcp_ports
            if xx != False and yy != False:
                xx = int(xx)
                yy = int(yy)
                usage_common_used_port_list = False
                for ix in range(xx, yy):
                    sb = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socket.setdefaulttimeout(0.0000005)
                    ab = sb.connect_ex((self.hote, ix))
                    sleep(0.0000005)
                    sb.close()
                    if int(ab) == 0:
                        self.open_tcp_ports.append(ix)
                self.closed_tcp_ports.append((max(yy, xx)-min(yy,xx))-len(self.open_tcp_ports))
                return self.open_tcp_ports, self.closed_tcp_ports
