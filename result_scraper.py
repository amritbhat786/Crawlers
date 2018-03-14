from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#import bs4 
from bs4 import BeautifulSoup as bs
from urllib.request import Request,urlopen
import csv

'''
driver = webdriver.Chrome("/mnt/c/Program Files/chromedriver.exe")
driver.get("http://results.vtu.ac.in/vitaviresultnoncbcs/index.php")
'''
def get_result_page_info():
	req = Request("http://results.vtu.ac.in/vitaviresultnoncbcs/resultpage.php")
	with urlopen(req) as res:
		page = res.read()
		
	raw = bs(page,"html.parser")
	print(raw.prettify())
	with open("result_page_res.txt",'w') as f:
		f.write(raw.prettify())

		
def get_index_page_info():
	req = Request("http://results.vtu.ac.in/vitaviresultnoncbcs/index.php")
	with urlopen(req) as res:
		page = res.read()
		
	raw = bs(page,"html.parser")
	print(raw.prettify())
	with open("index_page_res.txt",'w') as f:
		f.write(raw.prettify())
	
def return_usn(reg_no):
	if reg_no<10:
		return "1pe14cs00"+str(reg_no)
	elif reg_no>=10 and reg_no<100:	
		return "1pe14cs0"+str(reg_no)
	else:
		return "1pe14cs"+str(reg_no)
	
def parse_marks(innerHTML):
	soup = bs(innerHTML,'html.parser')
	#print(soup.prettify())
	name_tag = soup.find("td",{"style":"padding-left:15px"})
	name = name_tag.text.split(":")[-1]
	div_tag = soup.find_all("div",{"class":"divTableCell"})
	index = 0
	for idx,val in enumerate(div_tag):
		if val.string.lower() == "programming the web":
			internal_index = idx+1
			external_index = idx+2
			total_index = idx+3
			break
	list_of_marks = [div_tag[internal_index].string,div_tag[external_index].string,div_tag[total_index].string]
	return name,list_of_marks	
		
def get_data_from_page():		
	driver = webdriver.Chrome("/mnt/c/Program Files/chromedriver.exe")
	driver.get("http://results.vtu.ac.in/vitaviresultnoncbcs/index.php")
	csvfile = "Web_marks.csv"
	with open(csvfile,"w") as file:
		col_names = ["Name","Internal","External","Total"]
		write_fd = csv.writer(file)
		write_fd.writerow(col_names)
		for reg_no in range(1,150):
			if reg_no not in [15,37,50,51,52,106,110,115,131]:
				elem = driver.find_element_by_name("lns")
				elem.clear()
				usn = return_usn(reg_no)
				try:
					elem.send_keys(usn)
					elem.send_keys(Keys.RETURN)
					innerHTML = driver.execute_script("return document.body.innerHTML")
					name,web_marks = parse_marks(innerHTML)
					write_row = [name,web_marks[0],web_marks[1],web_marks[2]]
					write_fd.writerow(write_row)
					back_button = driver.find_element_by_css_selector('#dataPrint > div:nth-child(3) > div:nth-child(1) > input')
					back_button.click()
					window_after = driver.window_handles[1]
					driver.switch_to_window(window_after)
				except:
					print("An error occured")
					alert = driver.switch_to.alert
					alert.accept()

if __name__ == "__main__":
	get_data_from_page()


