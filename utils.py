import os
import platform
import socket
from getpass import getuser
from subprocess import check_output

from lxml import etree
from requests import get


def Addpid(file="puids.txt"):
	file = str(file)
	if not file.endswith(".txt"):
		return False
	try:
		pid	= os.getpid()
		puids = open(file,"a")
		puids.write(str(pid)+"\n")
		puids.close()
	except PermissionError:
		print("[Error] Access denied for",file)
		if platform.system() == "Linux":
			print("Reload with '--sudo'")
		else:
			print("Run it as admin next time")
	except Exception as e:
		print(e)
		print("|Session unsaved|")
class Main():
	mycostatus = False
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	ip = ""
	try:
		s.connect(('10.255.255.255', 1))
		local_ip = s.getsockname()[0]
	except:
		local_ip = ''
	finally:
		s.close()
	def __init__(self):
		ip = ""
		try:
			moninstance = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			moninstance.connect(("8.8.8.8", 80))
		except:
			self.mycostatus = False
		else:
			self.mycostatus = True
		finally:
			moninstance.close()
	def IpDetails(self, target=ip, export=""):
		if self.mycostatus == True:
			details = get('http://ip-api.com/xml/{}'.format(str(target))).text
			nveaufichierxml = open("resultatip.xml", 'w')
			nveaufichierxml.write(str(details))
			nveaufichierxml.close()
			tree = etree.parse("resultatip.xml")
			for a in tree.xpath("/query/country"):
				country = a.text
			for b in tree.xpath("/query/countryCode"):
				countrycode = b.text
			for c in tree.xpath("/query/region"):
				region = c.text
			for d in tree.xpath("/query/regionName"):
				regionName = d.text
			for e in tree.xpath("/query/city"):
				city = e.text
			for f in tree.xpath("/query/zip"):
				zipcode = f.text
			for g in tree.xpath("/query/lat"):
				latitude = g.text
			for h in tree.xpath("/query/lon"):
				longitude = h.text
			for i in tree.xpath("/query/timezone"):
				timezone = i.text
			for j in tree.xpath("/query/isp"):
				ispname = j.text
			for k in tree.xpath("/query/org"):
				organization = k.text
			for l in tree.xpath("/query/as"):
				As = l.text
			for m in tree.xpath("/query/query"):
				cible = m.text
			print("   ---------------------{}---------------------".format(cible))
			print("01| Country > ", country)
			print("02| Country code > ", countrycode)
			print("03| Region > ", region)
			print("04| Region name > ", regionName)
			print("05| City > ", city)
			print("06| Zip code > ", zipcode)
			print("07| Latitude > ", latitude)
			print("08| Longitude > ", longitude)
			print("09| Timezone > ", timezone)
			print("10| Isp name > ", ispname)
			print("11| Organization > ", organization)
			print("12| As > ", As)
			print("   ---------------------------------------------------------")
			os.remove("resultatip.xml")#FileNotFoundError
			if export == "json":
				pass
			elif export == "txt":
				qsdf = open("ip_details.txt","w")
				qsdf.write(f"""
   ---------------------{cible}---------------------
01| Country > {country}
02| Country code > {countrycode}
03| Region > {region}
04| Region name > {regionName}
05| City > {city}
06| Zip code > {zipcode}
07| Latitude > {latitude}
08| Longitude > {longitude}
09| Timezone > {timezone}
10| Isp name > {ispname}
11| Organization > {organization}
12| As > {As}
   ---------------------------------------------------------
				""")
				qsdf.close()
	def PublicIpAddress(self):
		if self.mycostatus == True:
			self.ip = get('https://api.ipify.org').text
			return self.ip
	def MyPcDetails(self):
		self.ip = get('https://api.ipify.org').text
		pc_details = platform.uname()
		print("|________________________________________________________________|")
		print("")
		print("User:",getuser())
		if self.mycostatus == True:
			print("Internet access: OK")
			if self.local_ip != False:
				print("Local ip: ", self.local_ip)
			print("External ip: ", self.ip)
		if pc_details[1] != "":
			print("Name: ", pc_details[1])
		if pc_details[0] != "" and pc_details[2] != "":
			print("OS: ", pc_details[0], pc_details[2])
		if pc_details[3] != "":
			print("Version: ", pc_details[3])
		if pc_details[4] !="":
			print("Machine: ", pc_details[4])
		if pc_details[5] != '':
			print("Processor: ", pc_details[5])
		if platform.system() == 'Linux':
			distribu = platform.linux_distribution()
			if distribu[0] != "" and distribu[1] != "":
				print("Distrib: ", distribu[0], distribu[1])
			if distribu[2] != "":
				print("Id: ", distribu[2])
		print("")
		print("|________________________________________________________________|")
