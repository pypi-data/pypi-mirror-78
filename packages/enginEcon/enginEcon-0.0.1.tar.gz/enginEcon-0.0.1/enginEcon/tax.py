#depreciation
from .base import CashFlowBase
from matplotlib.pyplot import subplots
def straightLine(B,S,N,i):
    if N == 0:
        return B
    else:
        return B - i*(B-S)/N

def decliningBalance(B,R,N,i):
    return B*(1-R/N)**i

def sumOfYears(B,S,N,i):
    print(sum(range(N,N-i,-1)))
    print(sum(range(N)))
    return B - (B-S)*sum(range(N,N-i,-1))/(sum(range(N+1)))

class CapitalCashFlow(CashFlowBase):
    def __init__(self,capital,depreciations):
        #both should be sequences
        self.set_capdep(capital,depreciations)
    
    def set_capdep(self,cap,dep):
        cap,dep = self._validateSeq(cap),self._validateSeq(dep)
        self.cap,self.dep = self._equalize(cap,dep)
    
    def __add__(self,other):
        newCap,newDep = self._merge(self.cap,other.cap,self.dep,other.dep)
        return CapitalCashFlow(newCap,newDep)
    def __radd__(self,other):
        #needed for sum() to work
        return self
    
    def draw(self,labels=False,merge=False):
        return super().draw(self.cap,self.dep,labels=labels,merge=merge)

class AfterTaxCashFlow (CashFlowBase):
    # CashFlow __init__(self,seq=None,seq2=None)
    def __init__(self,BTCF,CapitalDepreciations,taxFunc):
        (self.BTCF_rev,
        self.BTCF_cos,
        self.cap,
        self.dep
        ) = self._equalize(
            BTCF.pos,
            BTCF.neg,
            CapitalDepreciations.cap,
            CapitalDepreciations.dep
        )
        self.taxFunc = taxFunc #tax func should return tax amount, not negative for summing
        self.calculateFlows()
    # def set_taxRate(self,rate):
    #     pass
    # def set_BTCF(self,BTCF):
    #     pass
    # def add_BTCF(self,BTCF):
    #     pass
    # def set_capdep(self,capdep):
    #     pass
    # def add_capdep(self,capdep):
    #     pass
    def calculateFlows(self):        
        self.taxableIncome = [i+j-k for i,j,k in zip(self.BTCF_rev,self.BTCF_cos,self.dep)]
        self.tax = [-self.taxFunc(i) if i>0 else 0 for i in self.taxableIncome ]
        self.ATCF_rev = self.BTCF_rev
        self.ATCF_cos = [i+j+k for i,j,k in zip(self.BTCF_cos,self.tax,self.cap)]
    
    def get_PW(self,rate):
        return self._get_PW(self.ATCF_rev,self.ATCF_cos,rate)
    def get_AW(self,rate):
        return self._get_AW(self.ATCF_rev,self.ATCF_cos,rate)
    def get_FW(self,rate):
        return self._get_FW(self.ATCF_rev,self.ATCF_cos,rate)
    def get_mergedSeries(self):
        return self._get_mergedSeries(self.ATCF_rev,self.ATCF_cos)
    def draw(self,labels=False,merge=False):
        return super().draw(self.ATCF_rev,self.ATCF_cos,labels=labels,merge=merge)


def createDepreciation(capital,n=0,depType=3):
    cap = [0]*n + [capital]
    if depType == 1:
        dep = [0]*(n+1) + [-capital]
    elif depType == 3:
        dep = [0]*(n+1) + [-capital/3]*3
    else:
        #dep = 
        #leaving room for other types of depreciations
        pass
    return CapitalCashFlow(cap,dep)