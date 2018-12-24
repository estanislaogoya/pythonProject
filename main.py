import requests
import dating
import datetime as dt
import data
import calendar

class Contract:
    def __init__(self, offer, settlement, symbol):
        self.price = offer
        self.settlement = settlement
        self.name = symbol
        self.month = 1
        self.year = int("20{y}".format(y=self.name[-2:]))
        self.setMonth()
        self.setMaturity()

    def setMonth(self):
        i = 0
        d = data.Data()
        for x in d.contractsRef:
            if x in self.name:
                self.month += i
                break
            i += 1

    def setMaturity(self):

        EOM = calendar.monthrange(self.year, self.month)[1]
        end_date = dt.datetime(self.year, self.month, EOM)

        dateList = dating.set_approach(dating.getDatesDiff(dt.datetime.now(), end_date), data.Data().arg_holidays)
        print("Year:{y} Month:{m} Maturity:{d}".format(d=len(dateList),y=self.year,m=self.month))
        self.maturity = len(dateList)

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
                r = requests.get(self.main_domain + url_instrumentos, headers=self.headers)
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

    def getDataBySegment(self):
        url_instrumentos = '/rest/instruments/bySegment?MarketSegmentID={msi}&MarketID={mid}'.format(msi='DDF',mid='ROFX')

        self.headers = { 'X-Auth-Token': self.rofex_token,
               "Content-Type": "application/json"
        }

        r = requests.get(self.main_domain + url_instrumentos, headers=self.headers)
        self.getValuesBySymbol(r.json()['instruments'])

if __name__ == "__main__":
    s = Session()
    s.authenticate()
    s.getDataBySegment()
