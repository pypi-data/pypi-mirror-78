from matplotlib.pyplot import subplots
from numpy import ndarray
from .interestTableFunctions import *
class CashFlowBase(object):
    def __init__(self):
        pass
        # for overriding
        # can be either capital depreciation or posneg
    
    def _equalize(self,*args):
        targetLen = max([len(i) for i in args])
        return tuple(i+[0]*(targetLen-len(i)) for i in args)
    def _validateSeq(self,seq):
        
        if type(seq) not in (list,tuple):
            raise SyntaxError("invalid seq type")
        #give up on validating items, if you want to enter invalid let the future errors enlighten you
        # if False in [type(i) in (float,int,ndarray,) for i in seq]:
        #     raise SyntaxError("invalid values in seq")
        return (list(seq) if type(seq)==tuple else seq)
    def _merge(self,a1,a2,b1,b2):
        #merge cashflows (1,2) on series (a,b) to make c1 and c2
        #eg self._merge(pos1,pos2,neg1,neg2)
        #assuming they start at the same time
        a1,a2 = self._equalize(a1,a2)
        b1,b2 = self._equalize(b1,b2)
        a3 = [i+j for i,j in zip(a1,a2)]
        b3 = [i+j for i,j in zip(b1,b2)]
        return a3,b3
        #return pos3,neg3

    def _get_PW(self,pos,neg,rate):
        return sum([PF(rate,i)*(pos[i]+neg[i]) for i in range(len(pos))])
    def _get_AW(self,pos,neg,rate):
        return self._get_PW(pos,neg,rate) * AP(rate,len(pos)-1)
    def _get_FW(self,pos,neg,rate):
        return self._get_PW(pos,neg,rate) * FP(rate,len(pos)-1)
    def _get_mergedSeries(self,pos,neg):
        return [pos[i]+neg[i] for i in range(len(pos))]


    def draw(self,pos,neg,labels=False,merge=False):
        fig,ax = subplots()
        xAxis = range(len(pos))
        if merge:
            merge = [i+j for i,j in zip(pos,neg)]
            up    = [i if i>0 else None for i in merge]
            down  = [i if i<0 else None for i in merge]
        else:
            up    =  [None if i== 0 else i for i in pos]
            down  =  [None if i== 0 else i for i in neg]
        try:# use_line_collection is not available in older version of matplotlib? idk
            ax.stem(xAxis,up,markerfmt="^",use_line_collection=True)
        except:
            ax.stem(xAxis,up,markerfmt="^")
        if labels:
            for i in range(len(xAxis)):
                if up[i]== None:
                    continue
                ax.text(xAxis[i],up[i]/20," $ {0:0.2f}".format(up[i]),
                    rotation=90,ha = "right",va='bottom')
        try:
            ax.stem(xAxis,down,markerfmt="rv",linefmt='r',use_line_collection=True)
        except:
             ax.stem(xAxis,down,markerfmt="rv",linefmt='r')
        if labels:
            for i in range(len(xAxis)):
                if down[i] == None:
                    continue
                ax.text(xAxis[i],down[i]/20," $ {0:0.2f}".format(down[i]),
                    rotation=90,ha = "right",va='top')
        #returning fig and subplot object for manual editing if desired
        return fig,ax

