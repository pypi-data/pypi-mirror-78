#Author : Priyanka Singh <ps21priyanka@gmail.com>

import pandas as pd
import numpy as np
def dropnull(dataframe,method=None,axis=None):
    """This function will drop null in three ways that is dropping all null in the entire dataframe,dropping columns or rows having all nulls and dropping the rows or columns having any of the value as null and return the dataframe after removing null by the method as mentioned by user
     By default it drops all the null if no method is mentioned explicitely
    Parameters:
   
    1. dataframe : Dataframe on which the user want to drop nulls
    2. method(str) : Three methods : "all_null","rc_all_null","rc_any_null"
                    (i) "all_null" : This will drop all the nulls in entire dataframe despite rows or columns
                    (ii) "rc_all_null" : This will drop the columns or rows having all its value as Null or NaN or None
                        example 
                        row : NaN | NaN | NaN | NaN | NaN  ---> all values are null(hence it will be dropped)
                        column : Name  ---> column "name" has all value null so this will be dropped 
                                 ____
                                 NaN
                                 ____
                                 NaN
                                 ____
                                 NaN
                                 ____
                                 NaN
                                 ____
                                 NaN
                                 ____
                     (iii) "rc_any_null" : This will drop columns or rows having any of the value as Null or NaN or None
    3. axis(int) : It takes two value either 1 or 0 , 1 for columns and 0 for rows
    
     
    How to call function(demo):
    
   
    1. res = dropnull(df,"rc_all_null",1) --> this will drop the columns whose 
                                                         entire value is null
       res = dropnull(df,"rc_all_null",0) --> this will drop the rows whose 
                                                         entire value is null
    2. res = dropnull(df,"rc_any_null",1) --> this will drop the columns whose 
                                                         atleast one value is null
       res = dropnull(df,"rc_any_null",0) --> this will drop the rows whose 
                                                         atleast one value is null
    
    Returns:
    Dataframe : returning dataframe by removing nulls with the method mentioned by the user"""
    
    #to drop all null across all rows and columns
    if ((method == None) and (axis==None)):   
        result = dataframe.dropna()
    #to drop rows and columns having all values as null to drop rows having all nulls using axis=0 and for dropping columns having all values null,use axis=1
    elif method == "rc_all_null":
        result = dataframe.dropna(how = 'all',axis=axis)
    #to drop rows and columns having atleast one null value, to drop rows having atleast one null use axis=0 and for dropping columns having one null,use axis=1
    elif method == "rc_any_null":
        result = dataframe.dropna(how = 'any',axis=axis)
    return result
   


def dropnull_th(dataframe,percentage):
    """This function will drop the nulls in those columns where the number of nulls is greater than or equal to the percentage specified by the user and returns dataframe having nulls dropped in those columns where number of null is greater than the percentage(mentioned by user while calling function) of total number of records in that column
    
    Parameters:
    
    1. dataframe : Dataframe where you want to drop columns where the number of null is greater than some percentage value
    2. percentage(int) : Threshold percentage value set by user
    
    Methodology: 
    If user sets perentage as 60
    then the column where the number of null is greater than 60% of total number of records of the column, will be Dropped
    
    How to call function(demo):
    
    res = dropnull_th(df,20) --> res is the dataframe where you will be stroing the 
                                     output of this function
                                     df:your intial dataframe name
                                     20:your threshold percentage value
    Returns:
    Dataframe : returning dataframe by removing columns as per the threshold percentage value of nulls"""
    
    col=dataframe.columns.tolist()
    d = { c : dataframe[c].isnull().sum() for c in col }
    to_drop = [k for k, v in d.items() if v >= ((percentage * dataframe.shape[0])/100)]
    result = dataframe.drop(to_drop,axis=1)
    return result

def swapnull(dataframe,method="mean",num_val=0,char_val="unknown"):
    
    """This function will replace all the null values with the three different methods like
    custom method,mean and median and it will return the dataframe having all null values replaced
    by the method as chosen by the user.
    By default if nothing is mentioned explicitely,it will impute nulls with the mean value
     
    Parameters:
   
    1. dataframe : Dataframe on which the user want to do cleaning or preprocessing
    2. method (string) : Always quote inside(""), also by deafult the method to impute null value is mean
                      There are three ways in which you can impute:
                      1. method = "mean" - Method in which null values of numerical columns will get replaced with mean of that column
                      2. method = "median" - Method in which null values of numerical columns will get replaced with median of that column
                      3. method = "custom" - In this method user can explicitely decide value for numerical column like any integer or float number and value for categorical or object or string column as "unknown","not defined" .By default the value is 0 for numeric columns and "unknown" for string or object or categorical columns
    3. num_value(int or float) : Use this with method = "custom",not necessary with mean or median
                                 By default its value is 0 (for numerical columns)
    4. char_val(str) :  Use this with method = "custom",not necessary with mean or median
                        By default its value is "unknown" (for categorical columns(str,obj))
   
    How to call function(demo):
    
    1. for method = "custom"
    res=swapnull(df,"custom",1,"not known")
    res
    2. for method = "mean"
    res=swapnull(df)
    res
    3. for method = "median"
    res=swapnull(df,"median")
    res
    
    Returns:
    Dataframe : returning dataframe with all imputations done for null values"""
    
    if method == "custom":
        result = dataframe.apply(lambda x: x.fillna(num_val) if x.dtype.kind in 'biufc' else x.fillna(char_val))
    elif method == "mean":
        result = dataframe.apply(lambda x: x.fillna(round(x.mean(axis=0),2)) if x.dtype.kind in 'biufc' else x.fillna(char_val))
    elif method =="median":
        result = dataframe.apply(lambda x: x.fillna(x.median(axis=0)) if x.dtype.kind in 'biufc' else x.fillna(char_val))
    return result
def swapnull_subset(dataframe,columns,method="mean",num_val=0):
    
    """This function will replace all the null values in the columns as specified by the user with the three different methods like
    custom method,mean and median and it will return the dataframe having all null values replaced  in the selected columns
    by the method as chosen by the user.
    By default if nothing is mentioned explicitely,it will impute nulls with the mean value

    Parameters:
   
    1. dataframe : Dataframe on which the user want to do cleaning or preprocessing
    2. columns(list) : columns where you want your null values to be replaced
    3. method (string) : Always quote inside(""), also by deafult the method to impute null value is mean
                      There are three ways in which you can impute:
                      1. method = "mean" - Method in which null values of numerical columns will get replaced with mean of that column
                      2. method = "median" - Method in which null values of numerical columns will get replaced with median of that column
                      3. method = "custom" - In this method user can explicitely decide value for numerical column like any integer or float number and value for categorical or object or string column as "unknown","not defined" .By default the value is 0 for numeric columns and "unknown" for string or object or categorical columns
    4. num_value(int or float) : Use this with method = "custom",not necessary with mean or median
                                 By default its value is 0 (for numerical columns)
    5. char_val(str) :  Use this with method = "custom",not necessary with mean or median
                        By default its value is "unknown" (for categorical columns(str,obj))
   
    How to call function(demo):
    
    1. for method = "custom"
    res=swapnull_subset(df,['a','b'],"custom",1,"not known")
    df - name of dataframe where you want to perform imputation
    ['a','b'] - name of columns in dataframe df
    res
    2. for method = "mean"
    res=swapnull_subset(df,['a','b'])
    res
    3. for method = "median"
    res=swapnull_subset(df,['a','b'],"median")
    res
    
    Returns:
    Dataframe : returning dataframe with all imputations done for null values

    """   

    if method=="mean":
        dataframe[columns] = dataframe[columns].apply(lambda x: x.fillna(round(x.mean(),2)) if x.dtype.kind in 'biufc' else x.fillna(char_val))
    elif method == "custom":
        dataframe[columns] = dataframe[columns].apply(lambda x: x.fillna(num_val) if x.dtype.kind in 'biufc' else x.fillna(char_val))
    elif method =="median":
        dataframe[columns] = dataframe[columns].apply(lambda x: x.fillna(round(x.median(),2)) if x.dtype.kind in 'biufc' else x.fillna(char_val))
    return dataframe
        


