import requests
from os import path
from bs4 import BeautifulSoup
import sys
#from flask import Flask

dob = 123
roll_no = 12
login_url = 'http://alliancebschool.org/studentportal/aced/results/php/results.php?page=btech6b1519jun18'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0'}

def login(dob,roll_no):
	global path 
	path= "/home/ashwarya.shand/Desktop/task/"+str(dob)+"_"+str(roll_no)+".html"
	values = {
	'tregno': '123',
	'tdob': '01012000',
   	'submit':'+Get+Result+',
	}
	with requests.Session() as s:
		res = s.get(login_url,headers=headers)
		r = s.post(login_url, data=values,headers=headers)
		soup = BeautifulSoup(r.text, 'html.parser')
		tbody = soup.find('table', align='center')
		upload_file(r.content)
		return path,r.content

def upload_file(content):
	with open(path,"wb") as f:
		f.write(content)

if __name__ == "__main__":
	login(dob,roll_no)
	
