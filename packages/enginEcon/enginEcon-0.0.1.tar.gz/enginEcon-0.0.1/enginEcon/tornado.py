import matplotlib.pyplot as plt
import numpy as np

def calcTornado(data,func):
    '''creates outdata dict corresponding to order of indata dict

    parameters  :
        func    :   objective function --> func(a,b)
        indata  :   {'a':(a_min,a_mean,a_max),'b':(b_min,b_mean,b_max)}
    
    output  :   {'a':(func(a_min,b_mean) , func(a_mean,b_mean) , func(a_max,b_mean),
                 'b':(func(a_mean,b_min) , func(a_mean,b_mean) , func(a_mean,b_max)}'''
    indata = {k:sorted(v) for k,v in data.items()}
    outdata = data.copy()
    variables = func.__code__.co_varnames[:func.__code__.co_argcount]
    basevar = tuple(indata[v][1] for v in variables)
    baseOut = func(*basevar)
    for variable in variables:
        outdata[variable] = (
        func(*basevar[:variables.index(variable)] +(indata[variable][0],)+ basevar[variables.index(variable)+1:])
        ,baseOut
        ,func(*basevar[:variables.index(variable)] +(indata[variable][2],)+ basevar[variables.index(variable)+1:])
        )
    return outdata

def singleTornado(indata,*outdata):
    '''drawing a single tornado diagram
    
    parameters  :
        indata  :   indata dictionary
        outdata :   outdata dictionary
        
    output      :   fig,ax
                    matplotlib subplot axes and figure'''
    indata = {k:sorted(v) for k,v in indata.items()}
    fig,ax = plt.subplots()
    barThickness = 1
    yTicks = [barThickness*i*2 for i in range(len(indata.keys()))]
    
    #settle outdata[0]
    sOutData0 = sorted(
        outdata[0].items(),
        key = lambda x: abs(x[1][2] - x[1][0]),
    )
    
    for i in sOutData0:
        ax.set_xmargin(0.2)
        low = min(i[1][0],i[1][2])
        high = max(i[1][0],i[1][2])
        size = high-low
        ax.broken_barh(
            [(low , size)],
            (yTicks[sOutData0.index(i)],barThickness),
            alpha=0.5
            )

        ax.text(
            low,
            yTicks[sOutData0.index(i)],
            f" {i[0]} = {indata[i[0]][i[1].index(low)]} ",
            ha='right')
        
        ax.text(
            low,
            1+yTicks[sOutData0.index(i)],
            f" {low} ",
            ha='right',
            va='top')
        
        ax.text(
            high,
            yTicks[sOutData0.index(i)],
            f" {i[0]} = {indata[i[0]][i[1].index(high)]} ",
            ha='left')

        ax.text(
            high,
            1+yTicks[sOutData0.index(i)],
            f" {high} ",
            ha='left',
            va='top')

    ax.set_yticks([i+0.5*barThickness for i in yTicks])
    ax.set_yticklabels([i[0] for i in sOutData0])
    ax.axvline(sOutData0[0][1][1], color='black')
    return fig,ax

def multiTornado(indata,*outdata):
    '''drawing a tornado comparison diagram

    parameters:
        indata  :   indata dictionary
        outdata :   outdata dictionary
        
    output      :   fig,ax
                    matplotlib subplot axes and figure'''
    
    indata = {k:sorted(v) for k,v in indata.items()}
    fig,ax = plt.subplots()
    barThickness = 1
    yTicks = [barThickness*i*2 for i in range(len(indata.keys()))]
    #settle outdata[0]
    sOutData0 = sorted(
        outdata[0].items(),
        key = lambda x: abs(x[1][2] - x[1][0]),
    )
    factorOrder = [i[0] for i in sOutData0]
    n = 0
    for i in sOutData0:
        ax.set_xmargin(0.2)
        low = min(i[1][0],i[1][2])
        high = max(i[1][0],i[1][2])
        size = high-low
        ax.broken_barh(
            [(low , size)],
            (yTicks[sOutData0.index(i)],barThickness),
            alpha=0.5,
            label = 'model '+str(n),
            color = 'C'+str(n)
            )
    n+=1

    for t in outdata[1:]:
        for i in [i[0] for i in sOutData0]:
            ax.set_xmargin(0.2)
            low = min(t[i][0],t[i][2])
            high = max(t[i][0],t[i][2])
            size = high-low
            ax.broken_barh(
                [(low , size)],
                (yTicks[factorOrder.index(i)],barThickness),
                alpha=0.75,
                label = 'model '+str(n),
                color = 'C'+str(n)
                )
        n+=1
    
    h,l = ax.get_legend_handles_labels()
    h_,l_ = [],[]
    for i in range(len(h)):
        if l[i] not in l_:
            h_.append(h[i])
            l_.append(l[i])
    ax.legend(h_,l_)
    ax.set_yticks([i+0.5*barThickness for i in yTicks])
    ax.set_yticklabels([i[0] for i in sOutData0])
    ax.axvline(sOutData0[0][1][1], color='black')
    return fig,ax

def drawTornado(dataset, *functions):
    '''general wrapper for all the drawing functions

    parameters  :
        datasets    :   dictionary inputs --> {variable name:(min,mean,max)}
        functions   :   objective functions
                        One function draws a single Tornado diagram
                        Multiple functions draws a Tornado comparison diagram
    '''
    if len(functions) == 1:
        return singleTornado(dataset , calcTornado(dataset,functions[0]))
    elif len(functions) > 1:
        return multiTornado(dataset, *[calcTornado(dataset,i) for i in functions])
    else:
        raise SyntaxError('no functions provided')