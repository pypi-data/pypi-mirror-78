#Author : Priyanka Singh<ps21priyanka@gmail.com>

import numpy as np
import scipy.stats as st
from tqdm import tqdm
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

def fit_distributions(dataframe,column,bins=100):
    
    # Returns un-normalised (i.e. counts) histogram

    array = dataframe[column].dropna().tolist()
    y, x = np.histogram(np.array(array), bins=bins)
    
    # Some details about the histogram
    bin_width = x[1]-x[0]
    N = len(array)
    x_mid = (x + np.roll(x, -1))[:-1] / 2.0 # go from bin edges to bin middles
    
    # selection of available distributions
    # CHANGE THIS IF REQUIRED
    DISTRIBUTIONS = [st.beta,
              st.expon,
              st.gamma,
              st.lognorm,
              st.norm,
              st.pearson3,
              st.triang,
              st.uniform,
              st.weibull_min, 
              st.weibull_max]


    # loop through the distributions and store the sum of squared errors
    # so we know which one eventually will have the best fit
    sses = []
    for dist in tqdm(DISTRIBUTIONS):
        name = dist.__class__.__name__[:-4]

        params = dist.fit(np.array(array))
        arg = params[:-2]
        loc = params[-2]
        scale = params[-1]

        pdf = dist.pdf(x_mid, loc=loc, scale=scale, *arg)
        pdf_scaled = pdf * bin_width * N # to go from pdf back to counts need to un-normalise the pdf

        sse = np.sum((y - pdf_scaled)**2)
        sses.append([column,sse, name])

    # Things to return - df of SSE and distribution name, the best distribution and its parameters
    results = pd.DataFrame(sses, columns = ['Column','SSE','distribution']).sort_values(by='SSE') 
    results=results.nsmallest(3,'SSE')
    
    
    return results

def distr_summ(dataframe):
    """This function is used to know the distribution of every numeric column having continuous values
    
    Parameters:
    dataframe : name of the dataframe on which you want to know the distribution
    
    How to call function(demo) : 
    res = distr_summ(df)
    res
    Returns:
    Dataframe returning the top 3 distribution for every numeric columns"""
    a=[]
    result = pd.DataFrame()
    for x in dataframe.columns:
        if 1.*dataframe[x].nunique()/dataframe[x].count() >0.1:
            a.append(x)
    df1 =dataframe[a]
    cols = df1.select_dtypes([np.number]).columns
    for x in cols:
        res=fit_distributions(df1,x,bins=100)
        result = result.append(res) 
    result = result.reset_index()
    result= result.drop('index',axis=1)
    return result
