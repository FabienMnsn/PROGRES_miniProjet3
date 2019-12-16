import requests
import re


def request_author_file_builder(author_name):
	# author_name = "First_Name Last_Name"
	"""
	returns a perfectly splelled url to get de xml file containing all publications of 'author_name'
	"""
	author_name_split = author_name.split(' ')
	last_name_cut = author_name_split[1][0].lower()
	request = "https://dblp.uni-trier.de/pers/xx/"+last_name_cut+"/"+author_name_split[1]+":"+author_name_split[0]+".xml"
	return request


def download_file(author_name, download_path):
	requested = requests.get(request_author_file_builder(author_name))
	if(requested.status_code == 200):
		with open(download_path+""+author_name+".xml", 'wb') as local_file:
			for chunk in requested.iter_content(chunk_size=128):
				local_file.write(chunk)
		local_file.close()
	else:
		print(requested.status_code)

if __name__ == '__main__':
	download_file("Julien Sopena", "XML/")