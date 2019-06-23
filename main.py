import requests
import dating
import datetime as dt
import data
import calendar
import random

MAE = 38

class Contract:
    def __init__(self, offer, settlement, symbol):
        self.price = offer
        self.settlement = settlement
        self.name = symbol
        self.month = 1
        self.year = int("20{y}".format(y=self.name[-2:]))
        self.setMonth()
        self.setDuration()
        print(self.getImplicitRate())

    def setMonth(self):
        i = 0
        d = data.Data()
        for x in d.contractsRef:
            if x in self.name:
                self.month += i
                break
            i += 1

    def setDuration(self):

        EOM = calendar.monthrange(self.year, self.month)[1]
        end_date = dt.datetime(self.year, self.month, EOM)

        dateList = dating.set_approach(dating.getDatesDiff(dt.datetime.now(), end_date), data.Data().arg_holidays)
        print("Year:{y} Month:{m} Duration:{d}".format(d=len(dateList),y=self.year,m=self.month))
        self.duration = len(dateList)

    def getImplicitRate(self):
        #Hardcoded
        self.price = random.randint(39,50)
        print(self.price)
        IR = ((self.price/MAE)-1)*365/self.duration
        return '{:.1%}'.format(IR)

class Session:
    def __init__(self):
        self.main_domain = 'http://pbcp-remarket.cloud.primary.com.ar'
        self.username = "tanigoya365"
        self.password = "Primary1+"
        self.headers = { "X-Username": self.username,
                   "X-Password": self.password,
                   "Content-Type": "application/json"
        }

    def authenticate(self):
        r = requests.post(self.main_domain + '/auth/getToken', headers=self.headers)
        self.rofex_token = r.headers['X-Auth-Token']
        self.headers = { 'X-Auth-Token': self.rofex_token,
               "Content-Type": "application/json"
            }

    def callApiGet(self, url):
        return requests.get(self.main_domain + url, headers=self.headers)

class Main:
    def __init__(self):
        self.session = Session()
        self.session.authenticate()
        self.getDataBySegment()

    def getDataBySegment(self):
        url_instrumentos = '/rest/instruments/bySegment?MarketSegmentID={msi}&MarketID={mid}'.format(msi='DDF',mid='ROFX')
        r = self.session.callApiGet(url_instrumentos)
        self.getValuesBySymbol(r.json()['instruments'])

    def getValuesBySymbol(self, instruments):
        symbols = []
        for x in instruments:
            symbols.append(x['symbol'])

        d = data.Data()
        if d.marketClosed:
            print("market closed")
        else:
            r = dating.getDatesDiff(dt.datetime.now(), dt.datetime(2018, 12, 31))
            dating.set_approach(r, d.arg_holidays)
            fil_symbols = set(symbols) & set(d.getContracts())
            #Buscar valores via API para cada symbol
            array = []
            for x in fil_symbols:
                url_instrumentos = '/rest/marketdata/get?marketId=ROFX&symbol={sym}&entries=BI,OF,LA,OP,CL,SE,OI'.format(sym=x)
                r = requests.get(self.session.main_domain + url_instrumentos, headers=self.session.headers)
                symbol = x
                try:
                    price = r.json()['marketData']['OF'][0]['price']
                except:
                    price = "NA"

                try:
                    settlement = r.json()['marketData']['SE']['price']
                except:
                    settlement = "NA"

                obj = Contract(price, settlement, symbol)
                array.append(obj)

            for obj in array:
                print(obj)

if __name__ == "__main__":
    #Main()
