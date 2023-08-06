'''
TODO
--calculations--
continual compounding on the interestTables

--cash flow analysis--
b/c analysis
mirr
'''
#some thing just don't need to be improved
from numpy import irr #,mirr,nper,rate
from .interestTableFunctions import *
from .base import CashFlowBase

from . import tax

class CashFlow(CashFlowBase):
    def __init__(self,*seqs):
        #seq and seq2 to account for positive and negative flows
        self.set_sequence(seqs)

    def set_sequence(self,seqs):
        if len(seqs) == 0:
            raise SyntaxError("No sequences provided")
        seqs = [self._validateSeq(seq) for seq in seqs]
        flowLen = max((len(i)for i in seqs))
        pos = [0]*flowLen
        neg = [0]*flowLen
        for seq in seqs:
            for i in range(len(seqs[0])):
                if seq[i]>0:
                    pos[i] += seq[i]
                elif seq[i]<0:
                    neg[i] += seq[i]
        self.pos = pos
        self.neg = neg

        
    def __add__(self,other):
        newPos,newNeg = self._merge(self.pos,other.pos,self.neg,other.neg)
        return CashFlow(newPos,newNeg)
    def __radd__(self,other):
        #needed for sum() to work
        return self

    def get_PW(self,rate):
        return self._get_PW(self.pos,self.neg,rate)
    def get_AW(self,rate):
        return self._get_AW(self.pos,self.neg,rate)
    def get_FW(self,rate):
        return self._get_FW(self.pos,self.neg,rate)
    def get_mergedSeries(self):
        return self._get_mergedSeries(self.pos,self.neg)

    def rebase(self, newBase=1):
        if newBase<=1:
            raise SyntaxError("rebase can only be increased sorry :(")
        elif float(newBase) != int(newBase):
            raise SyntaxError("rebase has to be an integer")
        for i in self.pos:
            newPos += [i] + [0]*newBase-1
        for i in self.neg:
            newNeg += [i] + [0]*newBase-1
        return CashFlow(newPos,newNeg)

    def IRR(self, other=False):
        if other:
            if len(self.pos) != len(other.pos):
                raise SyntaxError("mismatched study periods, cannot calculate IRR")
            toCheck = [j-i for i,j in zip(self.get_mergedSeries(),other.get_mergedSeries())]
        else:
            toCheck = self.get_mergedSeries()
        return irr(toCheck)
    '''
    def MIRR(self, other=False):  #DO from scratch
        if other:
            toCheck = [j-i for i,j in zip(self.get_mergedSeries,other.get_mergedSeries)]
        else:
            toCheck = self.get_mergedSeries()
        #MIRR(toCheck)
        return "MIRR"
    def BC(self, other=False): #Do from scratch
        if other:
            #comparative
            return "compare"
        return "self BC"
    '''
    def draw(self,labels=False,merge=False):
        return super().draw(self.pos,self.neg,labels=labels,merge=merge)

#general instantiators
def createA(pmt=0,length=0):
    #raise error if length<0
    seq = [0]+[pmt]*length
    return CashFlow(seq)

def createB(pmt=0,length=0):
    #raise Error if length <0
    seq = [pmt]*length+[0]
    return CashFlow(seq)
                    
def createG(g=0,length=0):
    seq = [0]+[i*g for i in range(length)]
    return CashFlow(seq)

def createGeo(start=1,f=0,length=0):
    seq = [0]+[start*(1+f)**i for i in range(length)]
    return CashFlow(seq)

def createSingle(pos=0,value=0,length=0):
    seq = [0] *max(length+1,pos+1)
    seq[pos] = value
    return CashFlow(seq)

def createRepeat(pattern=[0],length=0):
    seq = [0] + (1+length//len(pattern))*pattern
    seq = seq[:length+1]
    return CashFlow(seq)

# other art pro

def drawCashFlows(*args):
    #take in a series of lists/tuples and draw a cash flow for them
    maxLen = max([len(i)for i in args])
    rebased = [i+[0]*(maxLen-len(i)) for i in args]
    pos = [0]*maxLen
    neg = [0]*maxLen
    for i in range(maxLen):
        for series in rebased:
            if series[i]>0:
                pos[i] += series[i]
            elif series[i]<0:
                neg[i] += series[i]
    print(pos,neg)
    fig,ax = CashFlow(pos,neg).draw()
    return fig,ax