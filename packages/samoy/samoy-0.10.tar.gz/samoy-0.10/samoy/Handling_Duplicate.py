#Author : Priyanka Singh<ps21priyanka@gmail.com>
#Author : Abhishek Pailwan<pailwan.abhishek22@gmail.com>
import pandas as pd
import numpy as np
def drop_replicatecols(dataframe):
    """This function will drop duplicate columns  and return the dataframe after dropping the columns
    having same name(names are also typographically matched with respect to upper or lower case)
     
    Parameters:
   
    dataframe : Dataframe on which the user want to drop its duplicate columns
     
     
    How to call function(demo):
    
    res = drop_replicatecols(df1)
    res
    
    Methodology :
    
    First thing this function does is it converts the dataframe columns names into all 
    lower case so as to tackle duplicate columns names like
    'First Score',
    'FIrsT ScorE',
    'fIRST sCORE',
    'FIRSt SCORe',
    'fiRST scORE' and then it only contains one column
    even if there is no need to convert lower case may the user have used same columns names then also this
    function will drop the duplicate columns

    
    Returns:
    Dataframe : returning dataframe with all duplicate columns being removed"""
    
    dataframe.columns = [x.lower() for x in dataframe.columns]
    res=dataframe
    res=res.loc[:,~res.columns.duplicated()]
    return res

from pandas.api.types import is_string_dtype

def drop_replicates(df,name=None):
    '''
    This function drops duplicate rows that are present in enitre column of dataframe or within the subset of columns as specifies by users
    
    Parameters:
       df (Data Frame) : The DataFrame which is to be used for dropping duplicates.
       name (List) : The list of subset of columns to be used for dropping duplicates.
                     By default it takes entire column set
    
    Returns:
       The DataFrame containing no duplicates row wise for entire set of columns or subset of columns
    
    
    '''
    if name:
        return drop_low(df,name,len(name)-1)
    else:
        return drop_low(df,list(df.columns),len(list(df.columns))-1)

def drop_low(df,name,n):
    '''
    Returns data with no duplicates as well as removes Typographical duplicate values.
    
    Parameters:
        df (Data Frame) : The DataFrame which is to be used for dropping duplicates.
        name (List) : The list of columns to be used for dropping duplicates.
        n (Int) : The integer value of length of the list which starts from 0.
        
    Returns:
        The DataFrame that was cleaned by dropping duplicate values.

    '''
    if n<0:
        df=df.drop_duplicates(subset = name)
        return df
        # is_string_dtype get used for object column detection.
    if is_string_dtype(name[n]):
        # converts columns to object that is string.
        df[name[n]]=df[name[n]].astype(str)
        # converts mentioned column to lower case.
        df[name[n]]=df[name[n]].str.lower()
    return drop_low(df,name,n-1)




"""def drop_duplicate_rows(dataframe):
    This function will remove duplicate rows after converting all values into either lower or upper case
     
    Parameters:
   
    dataframe : Dataframe on which the user want to drop its duplicate columns
     
     
    How to call function(demo):
    
    res = drop_duplicate_rows(df1)
    res

    Returns:
    Dataframe : returning dataframe with all duplicate rows being removed
    
    res = dataframe.apply(lambda x: x.astype(str).str.lower() if x.dtype.kind not in 'biufc' else x)
    res1 = res.drop_duplicates() 
    return res1"""

