from pyparsing import col
import requests
import os
from bs4 import BeautifulSoup
from tkinter import *
from datetime import date, datetime
import json
import time

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
TIME_TO_WAIT = 2 #seconds

MONTHS = \
{
'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04',
'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08',
'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'
}

#these are all the templates for the OFX format
class Templates:
    def OFX_header(datetime):
        return"""<?xml version="1.0" encoding="UTF-8"?>
<?OFX OFXHEADER="200" VERSION="200" SECURITY="NONE" OLDFILEUID="NONE" NEWFILEUID="NONE"?>
<OFX>
<!--Created by hleOfxQuotes on: Mon Dec 02 13:06:20 PST 2019-->
<SIGNONMSGSRSV1>
    <SONRS>
    <!--DTSERVER local time is Mon Dec 02 13:06:20 PST 2019-->
    <STATUS>
        <CODE>0</CODE>
        <SEVERITY>INFO</SEVERITY>
        <MESSAGE>Successful Sign On</MESSAGE>
    </STATUS>
    <DTSERVER>{datetime}</DTSERVER>
    <LANGUAGE>ENG</LANGUAGE>
    </SONRS>
</SIGNONMSGSRSV1>
<INVSTMTMSGSRSV1>
    <INVSTMTTRNRS>
    <TRNUID>1637E38B-EADA-4C16-A3EB-22947D5FCB36</TRNUID>
    <STATUS>
        <CODE>0</CODE>
        <SEVERITY>INFO</SEVERITY>
    </STATUS>
    <!--DTASOF local time is Mon Dec 02 13:00:01 PST 2019-->
    <INVSTMTRS>
        <DTASOF>{datetime}</DTASOF>
        <CURDEF>USD</CURDEF>
        <INVACCTFROM>
        <BROKERID>hungle.com</BROKERID>
        <ACCTID>0123456789</ACCTID>
        </INVACCTFROM>
        <INVPOSLIST>
""".format(datetime = datetime)

    def firstMutalFund(security, price, datetime):
        return"""                <POSMF>
            <!--DTPRICEASOF local time is Fri Nov 29 17:00:38 PST 2019-->
            <INVPOS>
            <!--Ticker from quote source is: CIBFX-->
            <SECID>
                <UNIQUEID>{symbol}</UNIQUEID>
                <UNIQUEIDTYPE>TICKER</UNIQUEIDTYPE>
            </SECID>
            <HELDINACCT>OTHER</HELDINACCT>
            <POSTYPE>LONG</POSTYPE>
            <UNITS>0.000</UNITS>
            <UNITPRICE>{price}</UNITPRICE>
            <MKTVAL>0.00</MKTVAL>
            <DTPRICEASOF>{datetime}</DTPRICEASOF>
            <!--Price currency is same as default currency-->
            <CURRENCY>
                <CURRATE>1.00</CURRATE>
                <CURSYM>USD</CURSYM>
            </CURRENCY>
            <MEMO>Price as of date based on closing price</MEMO>
            </INVPOS>
            <REINVDIV>Y</REINVDIV>
            <REINVCG>Y</REINVCG>
        </POSMF>
""".format(symbol = security.symbol, price = price, datetime = datetime)

    def secondMutualFund(security, price, datetime):
        return """      <MFINFO>
        <!--Ticker from quote source is: CIBFX-->
        <!--DTASOF local time is Fri Nov 29 17:00:38 PST 2019-->
        <!--Security is treated as Mutual Fund-->
        <SECINFO>
        <SECID>
            <UNIQUEID>{symbol}</UNIQUEID>
            <UNIQUEIDTYPE>TICKER</UNIQUEIDTYPE>
        </SECID>
        <SECNAME>{name}</SECNAME>
        <TICKER>{symbol}</TICKER>
        <UNITPRICE>{price}</UNITPRICE>
        <DTASOF>{date}</DTASOF>
        <!--Price currency is same as default currency-->
        <CURRENCY>
            <CURRATE>1.00</CURRATE>
            <CURSYM>USD</CURSYM>
        </CURRENCY>
        <MEMO>Price as of date based on closing price</MEMO>
        </SECINFO>
        <MFTYPE>OPENEND</MFTYPE>
    </MFINFO>
""".format(symbol = security.symbol, name = security.name, price = price, date = datetime)

    def firstStock(security, price, datetime):
        return """          <POSSTOCK>
            <!--DTPRICEASOF local time is Mon Dec 02 13:00:01 PST 2019-->
            <INVPOS>
            <!--Ticker from quote source is: BA-->
            <SECID>
                <UNIQUEID>{symbol}</UNIQUEID>
                <UNIQUEIDTYPE>TICKER</UNIQUEIDTYPE>
            </SECID>
            <HELDINACCT>OTHER</HELDINACCT>
            <POSTYPE>LONG</POSTYPE>
            <UNITS>0.000</UNITS>
            <UNITPRICE>{price}</UNITPRICE>
            <MKTVAL>0.00</MKTVAL>
            <DTPRICEASOF>{date}</DTPRICEASOF>
            <!--Price currency is same as default currency-->
            <CURRENCY>
                <CURRATE>1.00</CURRATE>
                <CURSYM>USD</CURSYM>
            </CURRENCY>
            <MEMO>Price as of date based on closing price</MEMO>
            </INVPOS>
            <REINVDIV>Y</REINVDIV>
        </POSSTOCK>
""".format(symbol = security.symbol, price = price, date = datetime)

    def secondStock(security, price, datetime):
        return """      <STOCKINFO>
        <!--Ticker from quote source is: BA-->
        <!--DTASOF local time is Mon Dec 02 13:00:01 PST 2019-->
        <!--Security is treated as Stock-->
        <SECINFO>
        <SECID>
            <UNIQUEID>{symbol}</UNIQUEID>
            <UNIQUEIDTYPE>TICKER</UNIQUEIDTYPE>
        </SECID>
        <SECNAME>{name}</SECNAME>
        <TICKER>{symbol}</TICKER>
        <UNITPRICE>{price}</UNITPRICE>
        <DTASOF>{date}</DTASOF>
        <!--Price currency is same as default currency-->
        <CURRENCY>
            <CURRATE>1.00</CURRATE>
            <CURSYM>USD</CURSYM>
        </CURRENCY>
        <MEMO>Price as of date based on closing price</MEMO>
        </SECINFO>
    </STOCKINFO>
""".format(symbol = security.symbol, name = security.name, price = price, date = datetime)

    def OFXSeperator():
        return"""        </INVPOSLIST>
        </INVSTMTRS>
        </INVSTMTTRNRS>
    </INVSTMTMSGSRSV1>
    <SECLISTMSGSRSV1>
        <SECLIST>
    """

    def OFXEnd():
        return"""    </SECLIST>
  </SECLISTMSGSRSV1>
</OFX>"""

class Security:
    def __init__(self, symbol, type, name) :
        self.symbol = symbol
        self.version = type
        self.name = name

class Main:
    def __init__(self):
        root = Tk()
        self.securities = self.loadSecurities()
        #create the labels for input fields
        labelDay = Label(root, text = "Select the day", anchor = 'w')
        labelMonth = Label(root, text = "Select the Month", anchor = 'w')
        labelYear = Label(root, text = "Select the year", anchor = 'w')
        labelName = Label(root, text = "File name\n(no extension)", anchor = 'w')

        #place labels
        labelDay.grid(row = 0, column = 0)
        labelMonth.grid(row = 1, column = 0)
        labelYear.grid(row = 2, column = 0)
        labelName.grid(row = 3, column = 0)

        #create entry variables
        self.selectedDay = StringVar()
        self.selectedMonth = StringVar()
        self.selectedYear = StringVar()
        self.entryName = Entry(root)

        #set initial values for entry variables
        today = str(date.today())
        key = [k for k, v in MONTHS.items() if v == today[5:7]][0]

        self.selectedDay.set(today[8:])
        self.selectedMonth.set(key)
        self.selectedYear.set(today[0:4])
        self.setName()

        #options for the drop menus
        dayOptions = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                      '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                      '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
        
        monthOptions = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        yearOptions = ['2021', '2022', '2023', '2024', '2025', '2026',
                       '2027', '2028', '2029', '2030', '2031', '2032', '2033']
        
        #create drop menus
        dayMenu = OptionMenu(root, self.selectedDay, *dayOptions, command = lambda event = None: self.setName())
        monthMenu = OptionMenu(root, self.selectedMonth, *monthOptions, command = lambda event = None: self.setName())
        yearMenu = OptionMenu(root, self.selectedYear, *yearOptions, command = lambda event = None: self.setName())

        #place option menus
        dayMenu.grid(row=0, column=1)
        monthMenu.grid(row=1, column=1)
        yearMenu.grid(row=2, column=1)
        self.entryName.grid(row=3, column=1)

        #create final options
        buttonTXT = Button(root, text = "Add/Remove symbol", command=lambda event=None: self.editSecurities(root))
        buttonOFX = Button(root, text = "create OFX", command=lambda event=None: self.createOFX())

        buttonTXT.grid(row = 4, column=0)
        buttonOFX.grid(row = 4, column=1)
        root.mainloop()

    def loadSecurities(self):
        f_in = open(CURRENT_DIRECTORY + "\\stockInfo.json", "r+")
        try:
            data = json.load(f_in)["Securities"]
            secObjects = []
            for security in data:
                secObjects.append(Security(security["symbol"], security["type"], security["name"]))
            return secObjects
        except Exception as e:
            writeError(e)

    def setName(self):
        day = self.selectedDay.get()
        month = MONTHS[self.selectedMonth.get()]
        year = self.selectedYear.get()
        filename = StringVar()
        filename.set(year + month + day + " quotes")
        self.entryName.configure(text = filename)

    def editSecurities(self, root):
        child = Toplevel(root)

        #lock parent window until this one is closed
        child.grab_set()

        #create labels for inputs
        Label(child, text = "Symbol").grid(row = 1, column = 0)
        Label(child, text = "type").grid(row = 2, column = 0)
        Label(child, text = "Name").grid(row = 3, column = 0)

        #create entries
        newSymbol = Entry(child)
        newName = Entry(child)
        newType = StringVar()
        typeOptions= ["MF", "Stock"]
        newType.set(typeOptions[0])
        typeField = OptionMenu(child, newType, *typeOptions)

        

        #place fields
        newSymbol.grid(row = 1, column = 1)
        typeField.grid(row = 2, column = 1)
        newName.grid(row = 3, column = 1)

        #create and place execution buttons
        Button(child, text="Remove Stock", command=lambda: 
               self.removeJson(child, newSymbol.get().upper().strip(), 
                               newType.get().strip(), 
                               newName.get().strip())).grid(row=4, column=0)
        
        Button(child, text="Add Stock", command=lambda: 
               self.addJson(child, newSymbol.get().upper().strip(), 
                            newType.get().strip(), 
                            newName.get().strip())).grid(row=4, column=1)

    def addJson(self, window, symbol, sType, name):
        self.clearEditMessage(window)
        for sec in self.securities:
            if sec.symbol == symbol:
                Label(window, text="Stock already in JSON", fg = "#FF0000").grid(row=5, column=0)
                return
            
        self.securities.append(Security(symbol, sType, name))
        self.securities.sort(key=lambda sec: sec.symbol)
        jsonString = json.dumps({"Securities": [tag.__dict__ for tag in self.securities]}, indent=4)
        f_out = open(CURRENT_DIRECTORY + "\\stockInfo.json", "w+")
        f_out.write(jsonString)
        f_out.close()

    def removeJson(self, window, symbol, sType, name):
        self.clearEditMessage(window)
        for sec in self.securities:
            if sec.symbol == symbol:
                self.securities.remove(sec)
                jsonString = json.dumps({"Securities": [tag.__dict__ for tag in self.securities]}, indent=4)
                f_out = open(CURRENT_DIRECTORY + "\\stockInfo.json", "w+")
                f_out.write(jsonString)
                f_out.close()
                return
        Label(window, text="Stock not in JSON", fg = "#FF0000").grid(row=5, column=0)
        return

    def clearEditMessage(self, window):
        for label in window.grid_slaves():
            if int(label.grid_info()["row"]) >=5:
                label.grid_forget()

    def createOFX(self):
        #get filename
        fileNameOFX = self.entryName.get() + ".ofx"

        #generate the day format used by Yahoo finance
        dd = self.selectedDay.get()
        if dd[0] == "0":
            day = dd[1]
        else:
            day = dd

        selectedDate = self.selectedMonth.get() + " " + day + ", " + self.selectedYear.get()

        #using selected date, create a dateTime to write into OFX file
        selectedDateTime = self.selectedYear.get() + MONTHS[self.selectedMonth.get()] + self.selectedDay.get() + "170000.000[-8:PST]"

        #OFX Files have parts with each stock/MF having a section in both
        # first we initialize the "header" values for each half
        OFX_firstHalf = Templates.OFX_header(selectedDateTime)
        OFX_secondHalf = Templates.OFXSeperator()

        #go through all selected securities
        for security in self.securities:
            time.sleep(TIME_TO_WAIT)
            currentSymbol = security.symbol
            print(currentSymbol)
            price = self.getClosePrice(selectedDate, currentSymbol)
            
            #If there was a valid value, add that to the halves
            if price != -1:
                ver = security.version
                if ver == "MF":
                    OFX_firstHalf += Templates.firstMutalFund(security, price, selectedDateTime)
                    OFX_secondHalf += Templates.secondMutualFund(security, price, selectedDateTime)
                
                elif ver == "Stock":
                    OFX_firstHalf += Templates.firstStock(security, price, selectedDateTime)
                    OFX_secondHalf += Templates.secondStock(security, price, selectedDateTime)
                
                else:
                    print("VERSION ERROR")

        #now we combine the 2 halves
        outputOFX = open(CURRENT_DIRECTORY + "\\" + fileNameOFX, "w+")
        outputOFX.write(OFX_firstHalf + OFX_secondHalf + Templates.OFXEnd())
        outputOFX.close()
        print("Done!\n")

    def getClosePrice(self, date, symbol):
        #send request to URL and validate response
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
        url = ("https://finance.yahoo.com/quote/%s/history?p=%s" %(symbol, symbol))
        result = requests.get(url, headers=headers)
        if result.status_code != 200:
            print("Response error from Yahoo")
            return -1
        
        try:
            #start scraping the data
            source = BeautifulSoup(result.content, "html.parser")
            valueTable = source.find("table", {"class":"table svelte-ewueuo"})
            #we include the [1:-1] to exclude the column names
            allDates = valueTable.find_all("tr")[1:-1]

            for datePoint in allDates:
                values = datePoint.find_all("td")

                #sometimes Yahoo puts divedends, we check the length to only get closing prices
                if date == values[0].text:
                    #sometimes Yahoo puts divedends, we check the length to only get closing prices
                    if len(values) <7:
                        print("Error 3: Date found with invalid format, continuing search")
                        continue
                    if isFloat(values[4].text):
                        print("entry for {symbol} found".format(symbol = symbol))
                        return float(values[4].text)
                    else:
                        print("Error 2: no valid data in selected date")
                        return -1
            print("Error 1: no entry for specified date")
            return -1     
        except Exception as e:
            print("An Error has occured with the Yahoo Webpage/servers")
            print("Press enter to exit the program as not to cause partially finished OFX files")
            print(e)
            input()
            exit()

def writeError(ex):
    now = datetime.now()
    filename = "\\" + now.strftime("%Y%m%d-%H%M") + ".txt"
    f_out = open(CURRENT_DIRECTORY + filename, "w+")
    f_out.write(ex)
    f_out.close()

def isFloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

Main()