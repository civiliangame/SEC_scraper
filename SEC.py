
from bs4 import BeautifulSoup
import requests
import xlwt


#Method that finds and stores all data into the excel document
def get_info(num, input_url):


    #Initiating the excel file
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Sheet 1")


    #Adding the correct columns
    sheet1.write(0, 0, "Release Number")
    sheet1.write(0, 1, "Date")
    sheet1.write(0, 2, "Action")
    sheet1.write(0, 3, "SEC Complaints")


    #Using Requests and BeautifulSoup
    r = requests.get(input_url)
    br = BeautifulSoup(r.content,"html.parser")
    #We find the table
    i=1
    for tr in br.find_all("tr", {"valign": "top"}):

        td = tr.find_all("td")
        if (len(td) != 3):
            continue
        for j in range(0, len(td)):
            if (td[j].get_text() == "Release No." or td[j].get_text() == "Date" or td[j].get_text() == "Action"):
                continue
            sheet1.write(i,j, td[j].get_text())
            for a in td[j].find_all("a"):
                try:
                    if(".pdf" in a.get("href")):
                        j+=1
                        sheet1.write(i, j, ("sec.gov"+ a.get("href")))
                        print("sec.gov" + a.get("href"))
                except Exception:
                    continue
        i+=1
    #save it to an excel file
    book.save(str(num) + "_Result.xls")

for i in range (1995,2016):
    get_info(i, "https://www.sec.gov/litigation/litreleases/litrelarchive/litarchive" + str(i) + ".shtml")