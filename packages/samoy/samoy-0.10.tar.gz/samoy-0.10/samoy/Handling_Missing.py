#Author : Abhishek Pailwan<pailwan.abhishek22@gmail.com>
import pandas as pd
pd.options.mode.chained_assignment = None
def replace(df1,df,name,n,method:None):
    '''
    This function replace NaN values with mean or median of the specific column. If user mention method as mean or median it will pick it as it is and if user dont want to mention any method then by default mean value to be replaced
    
    Parameters:
       df1 (Data Frame) : The DataFrame which is to be used for replacing NaN values
       df (Data Frame) : The data frame which contains data with required columns
       name (list) : The list of given columns to be modify
       n (int) : The length of the list
       method (str) : The specified method that is mean or median
       
    
    Returns:
       replace(df1,df,name,n,method) : The data frame with replaced NaN values with specified method and required columns
    
    
    '''
    if n<0:
        df1[name]=df
        return df1
    elif method == 'mean' or method == "None":
        df[name[n]]=df[name[n]].fillna(round(df[name[n]].mean(),2))
    elif method == 'median':
        df[name[n]]=df[name[n]].fillna(round(df[name[n]].median(),2))
    return replace(df1,df,name,n-1,method)

def swapmissing_subset(df,name,method):
    '''
    This function replace NaN values with mean or median in the specific columns only. If user mention method as mean or median it will pick it as it is and if user dont want to mention any method then by default missing value will be replaced to 
    mean value
    
    Parameters:
       df (Data Frame) : The DataFrame which is to be used for replacing NaN values
       name (list) : The list of given columns to be modify
       method (str) : The specified method that is mean or median
       
    
    Returns:
       swapmissing_subset(df,name,method) : The data frame with replaced NaN values with specified method and required columns
    
    '''
    df1=df[name]
    return replace(df,df1,name,len(name)-1,method)

def swapmissing(df,method):
    '''
    This function replace NaN values with mean or median of the specific column. If user mention method as mean or median it will pick it as it is and if user dont want to mention any method then by default mean value to be replaced
    
    Parameters:
       df (Data Frame) : The DataFrame which is to be used for replacing NaN values
       method (str) : The specified method that is mean or median
       
    
    Returns:
       swapmissing(df,method) : The data frame with replaced NaN values with specified method
    
    '''
    df1=df.select_dtypes(exclude=["bool_","object_"])
    return replace(df,df1,list(df1.columns),len(list(df1.columns))-1,method)

def lru(df,df1,name,n):
    """This function will replace the NaN value with last and next value of the same column and if there are many NaN values with start of the column then it will start replacing same with mean of the same column
     
    Parameters:
   
    1. dataframe (df): Dataframe on which the user want to do cleaning or preprocessing
    2. dataframe (df1): Dataframe which is taking only numerical data columns
    3. name (list) : The required columns of the data frame to be replaced with LRU function
    4. n (int) : Th integer value which is nothing but the length of the required list that is name
    
    Returns:
    Dataframe : returning dataframe with all imputations done for null values"""
    if n<0:     
        df1[name]=df
        return swapmissing(df1,'mean')
    else:
        lst=list(df.loc[pd.isna(df[name[n]]), :].index)
        ls=[]
        for i in lst:
            if i == 0:
                val=round(df[name[n]].mean(),2)
            else:
                val=round(df[name[n]][i-i:i+1].mean(),2)
            ls.append(val)
        df[name[n]][lst]=ls
        return lru(df,df1,name,n-1)
    
def swapmissing_lru(df):
    """This function will replace the NaN value with last and next value of the same column and if there are many NaN values with start of the column then it will start replacing same with mean of the same column
     
    Parameters:
   
    1. dataframe : Dataframe on which the user want to do cleaning or preprocessing
   
    Returns:
    Dataframe : returning dataframe with all imputations done for null values"""
    df1=df.select_dtypes(exclude=["bool_","object_"])
    return lru(df1,df,list(df1.columns),len(list(df1.columns))-1)


def drop_missing(df,name):
    '''
    This function drops missing values as well as NaN values from the given data.
    
    Parameters:
       df (Data Frame) : The DataFrame which is to be used for dropping missing and NaN values
       name (str) : The column name from which user want to drop missing and NaN values
       
    
    Returns:
       drop_missing(df,name) : The DataFrame which is to be clean by dropping missing and NaN values
    
    
    '''
    return df[df[name].astype(bool)].dropna(subset=[name])  

def drop_selected_missing(df,name,n):
    '''
    This function drops missing values as well as NaN values from the given data
    
    Parameters:
       df (Data Frame) : The DataFrame which is to be used for dropping missing and NaN values
       name (list) : The column name list from which user want to drop missing and NaN values
       n (int) : Integer value that represents length of the list
       
    
    Returns:
       drop_selected_missing(df,name,n) : The DataFrame which is to be clean by dropping missing and NaN values
    
    
    '''
    if n<0:
        return df.dropna(subset=name)
    else:
        return drop_selected_missing(df[df[name[n]].astype(bool)],name,n-1)
def dropmissing_subset(df,name):
    '''
    This function drops missing values as well as NaN values from the given data
    
    Parameters:
       df (Data Frame) : The DataFrame which is to be used for dropping missing and NaN values
       name (list) : The column name list from which user want to drop missing and NaN values
      
       
    
    Returns:
       dropmissing_subset(df,name) : The DataFrame which is to be clean by dropping missing and NaN values
    
    
    '''
    return drop_selected_missing(df,name,len(name)-1)
    
def dropmissing(df):
    '''
    This function drops missing values from the given data
    
    Parameters:
       df (Data Frame) : The DataFrame which is to be used for dropping missing and NaN values     
    
    Returns:
       dropmissing(df) : The DataFrame which is to be clean by dropping missing and NaN values
    
    
    '''
    return drop_selected_missing(df,list(df.columns),len(df.columns)-1)

def dropmissing_rows(df):
    '''
    This function drops rows whose all values are missing
    
    Parameters:
       df (Data Frame) : The DataFrame which is to be used for dropping missing and NaN values      
    
    Returns:
       dropmissing_rows(df) : The DataFrame which is to be clean by dropping missing and NaN values
    
    
    '''
    df=df.replace(r'^\s*$', np.nan, regex=True)
    return df.dropna(how='all')
   



 

   