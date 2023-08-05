from openpyxl import load_workbook
from cpa_std.ledger.tools import *
import os

class AccountName:
    def __init__(self):
        self.cur_dir=os.path.dirname(__file__)
        self.std_file = os.path.join(self.cur_dir, "account_std.xlsx")
        self.all=read_account_std_excel(self.std_file)
    @property
    def asset(self):
        return [i['name'] for i in self.all if i['kind']=="资产" or i['kind']=="资产或负债"]
    @property
    def liability(self):
        return [i['name'] for i in self.all if i['kind']=="负债" or i['kind']=="资产或负债"]
    @property
    def balanceSheet(self):
        return [i['name'] for i in self.all if i['kind'] == "资产" or i['kind'] == "资产或负债" or i['kind'] == "负债" or i['kind'] == "权益" ]
    @property
    def equity(self):
        return [i['name'] for i in self.all if i['kind']=="权益"]
    @property
    def income(self):
        return [i['name'] for i in self.all if i['kind'] == "利润表"]
    @property
    def cashFlow(self):
        return [i['name'] for i in self.all if i['kind'] == "现金流量表"]
    def match(self,name,kind=None):
        if kind==None:
            return best_match(name,self.all)
        elif kind=="asset":
            return best_match(name,self.asset)
        elif kind=="liability":
            return best_match(name,self.liability)
        elif kind == "equity":
            return best_match(name, self.equity)
        elif kind=="balanceSheet":
            return best_match(name,self.balanceSheet)
        elif kind == "incomeStatement":
            return best_match(name, self.income)
        elif kind == "cashFlow":
            return best_match(name, self.cashFlow)
if __name__ == '__main__':
    s=StdAcc()
    s.all
