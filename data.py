#data.py
import numpy as np
import datetime as dt
import dating

class Data:
    contractsRef = []
    def __init__(self):
        self.year = dt.datetime.now().year
        self.month = dt.datetime.now().month
        self.contractsRef = ['Ene',
                             'Feb',
                             'Mar',
                             'Abr',
                             'May',
                             'Jun',
                             'Jul',
                             'Ago',
                             'Sep',
                             'Oct',
                             'Nov',
                             'Dic']
        self.arg_holidays = ['2018-10-15',
                            '2018-11-19',
                            '2018-12-08',
                            '2018-12-24',
                            '2018-12-25',
                            '2018-12-31',
                            '2019-01-01',
                            '2019-03-04',
                            '2019-03-05',
                            '2019-03-24',
                            '2019-04-02',
                            '2019-04-18',
                            '2019-04-19',
                            '2019-05-01',
                            '2019-05-25',
                            '2019-06-17',
                            '2019-06-20',
                            '2019-07-08',
                            '2019-07-09',
                            '2019-08-17',
                            '2019-07-19',
                            '2019-10-12',
                            '2019-10-14',
                            '2019-11-18',
                            '2019-12-08',
                            '2019-12-25']

        if dt.datetime.now().weekday() == 1 or dt.datetime.now().weekday() == 7:
            self.marketClosed = True
        else:
            self.marketClosed = False

    def getContractAlone(self, position, year):
        if position > 12:
            position = position - 12

        return "DO{c}{y}".format(c=self.contractsRef[position-1],y=int(str(year)[-2:]))

    def getContracts(self):
        codes = []
        i = 0
        for _ in range(12):
            x = 0
            if (self.month + i) > 12:
                x = 1
            else:
                x = 0
            codes.append(self.getContractAlone(self.month + i, self.year + x))
            i += 1
        return codes
