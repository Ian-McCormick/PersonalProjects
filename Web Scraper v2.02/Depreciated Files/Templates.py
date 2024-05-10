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
    return"""
                    <POSMF>
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