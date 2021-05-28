from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv
import requests

START_URL="https://exoplanets.nasa.gov/exoplanet-catalog/"
browser=webdriver.Chrome("/Users/admin/Downloads/Code_Projects/c127/chromedriver_win32/chromedriver.exe")
browser.get(START_URL)
time.sleep(10)
headers=["name","light_years_from_earth","planet_mass","stellar_magnitude","discovery_date","hyperlink"]
planet_data=[]
new_planet_data=[]
def scrap():
    
    for i in range(0,439):
        while True:
            time.sleep(2)
            soup=BeautifulSoup(browser.page_source,"html.parser")
            current_page_number=int(soup.find_all("input",attrs={"class","page_num"})[0].get("value"))
            if current_page_number<i:
                 browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif current_page_number>i:
                 browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            else:
                break
        for ul_tag in soup.find_all("ul",attrs={"class","exoplanet"}):
            li_tags=ul_tag.find_all("li")
            temp_list=[]
    
            for index,li_tag in enumerate(li_tags):
                if index==0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            hyperlink_li_tag=li_tag[0]
            temp_list.append("https://exoplanets.nasa.gov/"+hyperlink_li_tag.find_all("a",href=True)[0]["href"])
            planet_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        print(f"{i} Page done 1")


def scrap_more_data(hyperlink):
    try:
        page=requests.get(hyperlink)
        temp_list=[]
        soup=BeautifulSoup(page.content,"html.parser")
        for tr_tag in soup.find_all("tr",attrs={"class":"fact_row"}):
            td_tags=tr_tag.find_all("td")
           
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div",attrs={"class":"value"})[0].contents[0])
                except:
                    temp_list.append("")
        new_planet_data.append(temp_list)
    except:
        time.sleep(1)
        scrap_more_data(hyperlink)

scrap()   

# for data in planet_data:
#     scrap_more_data(data[5])

final_planet_data=[]
for index,data in enumerate(planet_data):
    final_planet_data.append(data+final_planet_data[index])
with open("final.csv","w") as f:
    csvwriter=csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(final_planet_data)