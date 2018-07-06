
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


    #Initializing the counter for keeping track of rows
    i=1

    #Finding the "tr" tags directly since it's simplest this way

    #THE SEC WEBSITE IS TRASH AND THEY DON'T FORMAT HTML PROPERLY
    #Thus, the traditional method of narrowing down will not work, as the tables end where they should not.


    if(num < 2016 and num > 1998):
        tr_list = br.find_all("tr", {"valign": "top"})
    else:
        tr_list = br.find_all("tr")
    for tr in tr_list:
        #print(tr)
        #Then, find the "td" tags
        td = tr.find_all("td")
        #If it is the correct "td" tag, it should have three objects in it. Release Number, Date, and Action
        if (len(td) != 3):
            continue

        #a few "td" tags have the column names in it. We don't want this in our excel sheet.
        for j in range(0, len(td)):

            if (td[j].get_text() == "Release No." or td[j].get_text() == "Date" or td[j].get_text() == "Action"):
                continue

            #Write it into the excel spreadsheet
            sheet1.write(i,j, td[j].get_text())
            print(td[j].get_text())
            #We now want to find the "See also" parts
            for a in td[j].find_all("a"):

                #This part is prone to crash for some reason so let's do some error handling to prevent the entire code from crashing
                try:

                    #All the "See also" parts have a pdf file associated with it. We just want the pdf files.
                    #If it is a pdf file, add another column.
                    if(".pdf" in a.get("href")):
                        j+=1
                        sheet1.write(i, j, ("sec.gov"+ a.get("href")))

                #if the program was supposed to crash, just let it keep running.
                except Exception:
                    continue

        #Hop onto the next row.
        i+=1
    #save it to an excel file
    book.save(str(num) + "_Result.xls")

#Find everything
# #The website changes from 2016 onwards.
for i in range (1995,2019):
    if i == 2018:
        get_info(i, "https://www.sec.gov/litigation/litreleases.shtml")
    else:
        get_info(i, "https://www.sec.gov/litigation/litreleases/litrelarchive/litarchive" + str(i) + ".shtml")
    print(i)

#get_info(1995,"https://www.sec.gov/litigation/litreleases/litrelarchive/litarchive" + str(1995) + ".shtml" )