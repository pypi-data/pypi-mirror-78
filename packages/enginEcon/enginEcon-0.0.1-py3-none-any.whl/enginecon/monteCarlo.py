import scipy.stats as st
import numpy as np

# distributions return a array of size n if count=n
# else return an object
# object.rvs(n) to get an array of size n

# def discretePMF(values,probs,count=None):
#     if count:
#         return st.rv_discrete(values=(values,probs)).rvs(size=count)
#     else:
#         return st.rv_discrete(values=(values,probs))

def uniform(lower,upper,count=None):
    '''create a uniform continuous distribution between lower and upper

    parameters:
    lower   :   lower limit of distribution
    upper   :   upper limit of distribution
    count   :   None to create distribution
                Number to create sequence of n items distributed according to distribution'''
    if count:
        return st.uniform(loc=lower,scale = upper-lower).rvs(size=count)
    else:
        return st.uniform(loc=lower,scale = upper-lower)

def uniform_int(lower,upper,count=None):
    '''create a uniform discrete distribution between lower and upper inclusive (randint)

    parameters:
    lower   :   lower limit of distribution
    upper   :   upper limit of distribution
    count   :   None to create distribution
                Number to create sequence of n items distributed according to distribution'''
    if count:
        return st.randint(low=lower,high=upper+1).rvs(size=count)
    else:
        return st.randint(low=lower,high=upper+1)

def triangle(lower,mode,upper,count=None):
    '''create a triangular continuous distribution between lower and upper with peak at mode

    parameters:
    lower   :   lower limit of distribution
    mode    :   peak of triangle distribution
    upper   :   upper limit of distribution
    count   :   None to create distribution
                Number to create sequence of n items distributed according to distribution'''
    if count:
        return st.triang(loc=lower,c=(mode-lower)/(upper-lower),scale=upper-lower).rvs(size=count)
    else:
        return st.triang(loc=lower,c=(mode-lower)/(upper-lower),scale=upper-lower)

def normal(mean,stdvar,count=None):
    '''create a normal continuous distribution

    parameters:
    mean    :   mean of distribution
    stdvar  :   standard variation of distribution
    count   :   None to create distribution
                Number to create sequence of n items distributed according to distribution'''
    if count:
        return st.norm(loc=mean,scale=stdvar).rvs(size=count)
    else:
        return st.norm(loc=mean,scale=stdvar)

def trunc_normal(mean,stdvar,lower,upper,count=None):
    '''create a normal continuous distribution truncated to lower and upper 

    parameters:
    mean    :   mean of distribution
    stdvar  :   standard variation of distribution
    lower   :   lower truncation
    upper   :   upper truncation
    count   :   None to create distribution
                Number to create sequence of n items distributed according to distribution'''
    a,b = (lower - mean)/stdvar , (upper - mean)/stdvar
    if count:
        return st.truncnorm(a,b,loc=mean,scale=stdvar).rvs(size=count)
    else:
        return st.truncnorm(a,b,loc=mean,scale=stdvar)

def fixed(value,count=None):
    '''create a distribution of single value

    parameters:
    value    :   value of distribution
    count   :   None to create distribution
                Number to create sequence of n items distributed according to distribution'''
    if count:
        return st.uniform(loc=value,scale = 0).rvs(size=count)
    else:
        return st.uniform(loc=value,scale = 0)

def lognormal(mean,stdvar,count=None):    
    '''create a continuous lognormal distribution

    parameters:
    mean    :   value of lognormal distribution
    stdvar  :   standard variation of lognormal distribution
    count   :   None to create distribution
                Number to create sequence of n items distributed according to distribution'''
    a_mean = 0.5* np.log(mean**4/(stdvar**2+mean**2))
    a_stdvar = np.sqrt(np.log(stdvar**2/mean**2+1))
    if count:
        return st.lognorm(s=a_stdvar,scale=np.exp(a_mean)).rvs(size=count)
    else:
        return st.lognorm(s=a_stdvar,scale=np.exp(a_mean))

class risk(object):
    '''risk evaluation class'''

    def __init__(self,func,data,counts=None):
        '''parameters:
    func    (function)      :   objective function to evaluate
    data    (dictionary)    :   input data of form
    counts  (optional int)  :   number of simulations to run, defaults to size of smallest input array if possible, else 10000
    {
        variable:values
    }
        values can be distribution or sequence'''
        self.func = func
        self.data = data
        self.seq  = self.updateSeq(counts)
    def updateSeq(self,counts=None):
        '''runs function to create output data sequence'''
        self.errorCount = 0
        self.errorLog = []
        variables = self.func.__code__.co_varnames[:self.func.__code__.co_argcount]
        if not counts:
            countsList = []
            for i in self.data.values():
                try:
                    countsList += [len(i)]
                except:
                    countsList += [0]
            counts = max(countsList)
            if counts == 0:
                counts = 10000        
        sortedvars = ()
        for i in range(counts):
            ith = ()
            for key in variables:
                if type(self.data[key]) not in (list,tuple,np.ndarray):
                    ith += (self.data[key],)
                else:
                    ith += (self.data[key][i],)
            sortedvars+=(ith,)
        out = ()
        for i in sortedvars:
            try:
                out+=(self.func(*i),)
            except Exception as e:
                self.errorLog +=[e]
                self.errorCount+=1
        return np.array(out)
    def updateData(self,data):
        '''replace data,keep function and rerun simulation'''
        self.data = data
        self.seq = self.updateSeq()
    def updateFunc(self,func):
        '''replace function, keep data and rerun simulation'''
        self.func = func
        self.seq = self.updateSeq()
    def stats(self):
        '''give summary statistics for the simulation outputs'''
        return st.describe(self.seq)


    # return st.percentile updated version?
    def valueAtRisk(self,percentile):
        '''Calculate Value at Risk for the simualation results at percentile
        
        parameters:
            percentile  (str/float/int) :   percentile to calculate, ranging from 0 to 100
                                            able to take in as 10 or "10%"'''
        if type(percentile) == str:
            percentile = float(percentile.split('%')[0])
        VaR = np.percentile(self.seq,percentile)
        if VaR <0:
            return -VaR
        else:
            return 0


    def upsidePotential(self):
        '''calculates probability of result being >=0 for simulation results'''
        return len([i for i in self.seq if i >= 0])/len(self.seq)
        

    def downsideRisk(self):
        '''calculates probability of result being <0 for simulation results'''
        return len([i for i in self.seq if i < 0])/len(self.seq)

    # def tornado(self):
    #     if seq:
    #         seqStats = st.describe(seq)
    #         maxS,minS = seqStats.minmax
    #         meanS = seqStats.mean
    #     else:
    #         pass
        #pseduocode
        # subplot
        # for i in factors:
        #     a = [func(all expected values, linspace 10 i)]
        #     ax.plot(a)
        # # return fig,ax
        # return "This function is incomplete"