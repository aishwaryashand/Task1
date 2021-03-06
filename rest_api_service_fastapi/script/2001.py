import requests
from bs4 import BeautifulSoup
import os
from datetime import date

import constant
# from upload import upload_file

login_url = 'http://alliancebschool.org/studentportal/aced/results/php/results.php?page=btech6b1519jun18'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0'}

def login(params):
	if not os.path.exists(constant.path_to_file+str((date.today()).strftime("%y%m%d"))):
		os.mkdir(str((date.today()).strftime("%y%m%d")))
	path = constant.path_to_file+str((date.today()).strftime("%y%m%d"))+"/"+params.dob+"_"+params.roll_no+".html"

	values = {
		'tregno': params.roll_no,
		'tdob': params.dob,
		'submit':'+Get+Result+'
		}
	with requests.Session() as s:
		res = s.get(login_url,headers=headers)
		r = s.post(login_url, data=values,headers=headers)
		soup = BeautifulSoup(r.text, 'html.parser')
		response = soup.find('table', align='center').getText().strip()
		with open(path,"wb") as f:
			f.write(r.content)
		# result = upload_file(dob+".py","s3")
		return constant.html_file_path+path[path.find('rest'):],response

if __name__ == "__main__":
	login(dob,roll_no)
