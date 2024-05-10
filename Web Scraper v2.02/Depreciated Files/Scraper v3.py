import requests
from bs4 import BeautifulSoup
from tkinter import *
from datetime import date
import os

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

months = \
{
'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04',
'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08',
'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'
}

def gen_tags(): #creates a list of tags for scraping
    f_in = open(CURRENT_DIRECTORY + '\\tags.txt','r')
    stocks = f_in.readlines()
    f_in.close()
    tags = []
    for desc in stocks:
        seperate = desc.split(', ')
        tags.append(seperate)
    return tags

#create a URL given a tag
def url_gen(tag):
    url = ("https://finance.yahoo.com/quote/%s/history?p=%s" %(tag,tag))
    return url

#get the closing price based on a tag and date
def get_values(date, tag):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    result = requests.get(url_gen(tag), headers = headers)
    src = result.content
    soup = BeautifulSoup(src, 'html.parser')
    
    ptr = soup.findAll('tr')
    td = []
    data = [date, "-1"]
    for tr in ptr:
        if date in tr.text:
            td = tr.findAll('td')
            break
    if len(td) == 7:
        if isFloat(td[4].text):
            return [date, float(td[4].text)]
        else:
            print("ERROR 2: date exists, no valid value")
    else:
        print("Error 1: No entry for entered date")
    return [date, "-1"]

def isFloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def gen_date():
    month = months[mm.get()]
    datetime = yr.get()+month+dd.get()+'170000.000[-8:PST]'
    return datetime

def write2file():
    date = mm.get() + " " + dd.get() + ", " + yr.get()
    tags = gen_tags()
    open('data.txt','w+').close()
    f_out = open('data.txt', 'a')
    f_out.write(date + '\tClose Price\n')
    for tag in tags:
        print(tag[0])
        llist = get_values(date, tag[0])
        f_out.write(tag[0])
        f_out.write('\t\t')
        for line in llist:
            f_out.write(line[1] + '\t\n')
    f_out.close()
    print("\nDone!")

def edit_ofx(date, datetime, tag, ver):
    MF_temp1 = open(CURRENT_DIRECTORY + '\\MF_temp.txt', 'r').read()
    MF_temp2 = open(CURRENT_DIRECTORY + '\\MF_temp2.txt', 'r').read()
    S_temp1 = open(CURRENT_DIRECTORY + '\\Stock_temp.txt', 'r').read()
    S_temp2 = open(CURRENT_DIRECTORY + '\\Stock_temp2.txt', 'r').read()
    
    values = get_values(date, tag[0])
    if values[1] != "-1":
        unitprice = float(values[1])
        if ver == 'MF':
            #edits first part of OFX file
            first = (MF_temp1 %(tag[0], unitprice, datetime))
            
            #edits second part of OFX file
            second = (MF_temp2 %(tag[0], tag[2].rstrip(), tag[0], unitprice, datetime))
            
        elif ver == 'Stock':
            #edits first part of OFX file
            first = (S_temp1 %(tag[0], unitprice, datetime))
            
            #edits second part of OFX file
            second = (S_temp2 %(tag[0],tag[2].rstrip(), tag[0], unitprice, datetime))
    return [first, second]
    
def gen_heads(datetime):
    #generate first header
    f_in = open(CURRENT_DIRECTORY + '\\header.txt', 'r')
    header = f_in.read()
    first = (header %(datetime, datetime))
    f_in.close()
    
    #generate divider between first & second part of OFX file
    second ='''        </INVPOSLIST>
      </INVSTMTRS>
    </INVSTMTTRNRS>
  </INVSTMTMSGSRSV1>
  <SECLISTMSGSRSV1>
    <SECLIST>
'''
    return [first, second]
    
def combine(file, first, second):
    end = '''    </SECLIST>
  </SECLISTMSGSRSV1>
</OFX>'''
    f_out = open(CURRENT_DIRECTORY + '\\' + file, 'a+')
    f_out.write(first + second + end)
    f_out.close()
    
def mainOFX():
    day = dd.get()
    if day[0] == "0":
        day = day[1]
    else:
        day = day
    date = mm.get() + " " + day + ", " + yr.get()
    file_ofx = entryName.get() + '.ofx'
    datetime = gen_date()
    
    head = gen_heads(datetime)
    first = head[0]
    second = head[1]
    tags = gen_tags()
    
    for tag in tags:
        print(tag[0])
        ver = tag[1]
        data = edit_ofx(date, datetime, tag, ver)
        first += data[0]
        second += data[1]
    combine(file_ofx, first, second)
    print("\nDone!")

def set_name(self):
    name = StringVar()
    name.set(yr.get() + months[mm.get()] + dd.get() + " quotes")
    entryName.configure(text = name)
    
def main():
    root = Tk()
    #create the labels for input fields
    labelDay = Label(root, text = "Select the day", anchor = 'w')
    labelDay.grid(row = 0, column = 0)
    labelMon = Label(root, text = "Select the Month", anchor = 'w')
    labelMon.grid(row = 1, column = 0)
    labelYear = Label(root, text = "Select the year", anchor = 'w')
    labelYear.grid(row = 2, column = 0)
    labelName = Label(root, text = "File name\n(no extension)", anchor = 'w')
    labelName.grid(row = 3, column = 0)

    #create entry variables
    today = str(date.today())
    key = [k for k, v in months.items() if v == today[5:7]][0]
    global dd
    global mm
    global yr
    global entryName
    dd = StringVar()
    dd.set(today[8:])
    mm = StringVar()
    mm.set(key)
    yr = StringVar()
    yr.set(today[0:4])

    #create and put entry fields
    dropDay = OptionMenu(root, dd, '01', '02', '03', '04', '05', '06', '07', '08',
                         '09', '10', '11', '12', '13', '14', '15', '16', '17', '18',
                         '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31',
                         command = set_name)
    dropDay.grid(row = 0, column = 1)
    dropMon = OptionMenu(root, mm, "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", command = set_name)
    dropMon.grid(row = 1, column = 1)
    dropYear = OptionMenu(root, yr, '2021', '2022', '2023', '2024', '2025', '2026',
                          '2027', '2028', '2029', '2030', '2031', '2032', '2033', command = set_name)
    dropYear.grid(row = 2, column = 1)
    entryName = Entry(root)
    entryName.insert(END, yr.get() + months[mm.get()] + dd.get() + " quotes")
    entryName.grid(row = 3, column = 1)

    buttonOFX = Button(root, text = "Create OFX", command = mainOFX)
    buttonOFX.grid(row = 4, column = 1)
    buttonTXT = Button(root, text = "create TXT", command = write2file)
    buttonTXT.grid(row = 4, column = 0)

    root.mainloop()

main()
