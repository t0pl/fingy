# encoding: utf-8
import subprocess
from socket import socket,AF_INET, SOCK_STREAM, setdefaulttimeout, SOCK_DGRAM
from platform import system
from getpass import getuser
from sys import exit
import re

def GetLocalIp():
	# Credits: Openclassroom?
    s = socket(AF_INET, SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = False
    finally:
        s.close()
    return IP
def GetCurrentSSID():
	if system() == "Windows":
		try:
			ssid=subprocess.check_output(['netsh', 'wlan', 'show', 'networks']).replace("\r\n".encode(),"".encode()).split("SSID".encode())[1].split(": ".encode())[1].split("T".encode())[0].strip().decode()
			return ssid
		except Exception as e:
			print(e)
			print("An error occured while getting your ssid, check your connection and try again")
			return False
	elif system() == "Linux":
 		if getuser() == "root":
 			pass
#cat /etc/NetworkManager/system-connections/{ssid} | grep psk=
def GetPass():
	ssid = GetCurrentSSID()
	if ssid != None and ssid != False:
		if system() == "Windows":
			try:
				passwd = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', f'"{ssid}"', 'key=clear']).decode('utf-8', errors="ignore").split('\n')
				passwd = [b.split(":")[1][1:-1] for b in passwd if "Key Content" in b or "Contenu de la cl" in b]
			except subprocess.CalledProcessError:
				return False
			return passwd[0]
		elif system() == "Linux":
			passwd = subprocess.check_output(['cat', '/etc/NetworkManager/system-connections/{0}'.format(ssid)]).decode('utf-8').split('\n')
	else:
		return False
def GetFirstDigits():
	passwd = GetPass()
	if passwd != None and passwd != False:
		firstdigits = passwd[:8]
		return firstdigits
	else:
		return False
def Getdefaultgateaway():
	gateway = str(subprocess.check_output(['ipconfig'])).split("\\r\\n")
	for x in gateway:
		search = re.search(r"fau",str(x))
		if search:
			gateway = gateway[search.start():search.end()][0].split(" ")[-1]
			break
	return gateway
def GetDefaultGateway():
	try:
		gateway = str(subprocess.check_output(['ipconfig'])).encode('utf-8').decode('utf-8').split('\n')
		for x in gateway:
			if "Passerelle par d" in x:
				ipv6dfois = x.split("Passerelle par d")[1]
				ipv6dfois  = ipv6dfois.split("\\r\\n")[0]
				ipv6dfois = ipv6dfois.split(": ")[1]
				gateway = x.split()[-1][:-5]
				break
		if type(gateway) == str and gateway != '':
			return gateway
		elif type(ipv6dfois) == str and ipv6dfois != '':
			return ipv6dfois
		else:
			return False#Disconnected or Error(language,...)
	except:
		return False