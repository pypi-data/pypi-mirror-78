#Author : Priyanka Singh <ps21priyanka@gmail.com>

import pandas as pd
import numpy as np
def altercase(dataframe,method):
    """This function is usually to convert the content of dataframe either in lower case or upper case
    
    Parameters:
    1. dataframe : dataframe name where you want to change all its content as either lower or upper case
    2. method(str) : It has two options thats is either "lower" or "upper"

    How to call function(demo) : 
    1. altercase(df,"upper"): df -> name of your dataframe
                                    "upper" -> to convert every value string in upper case
    2. altercase(df,"lower"): df -> name of your dataframe
                                    "lower" -> to convert every value string in lower case
                                    
    Returns:
    Dataframe having its all values changed into either lower or upper case"""
    if method == "lower":
        return dataframe.apply(lambda x: x.astype(str).str.lower() if x.dtype.kind not in 'biufc' else x)
    elif method == "upper":
        return dataframe.apply(lambda x: x.astype(str).str.upper() if x.dtype.kind not in 'biufc' else x)
def altercase_subset(dataframe,columns,method):
    """This function is usually to convert the content of only selected columns either in lower case or upper case and returns dataframe having the content of mentioned columns either in lower or upper case
    
    Parameters:
    1. dataframe : dataframe name where you want to change all its content as either lower or upper case
    2. columns(list) : List of columns where you want the content to be either lower case or upper case
    3. method(str) : It has two options thats is either "lower" or "upper"

    How to call function(demo) : 
    1. altercase_subset(df,['a','b'],"upper"): df -> name of your dataframe
                                              ['a','b'] -> columns of dataframe df
                                             "upper" -> to convert every value string in upper case
    2. altercase_subset(df,['a','b'],"lower"): df -> name of your dataframe
                                              ['a','b'] -> columns of dataframe df
                                             "lower" -> to convert every value string in lower case
    Returns:
    Dataframe with the specified columns, having its value changesd into either lower or upper case"""
    if method=="lower":
        dataframe[columns] = dataframe[columns].apply(lambda x: x.astype(str).str.lower() if x.dtype.kind not in 'biufc' else x)
    elif method == "upper":
        dataframe[columns] = dataframe[columns].apply(lambda x: x.astype(str).str.upper() if x.dtype.kind not in 'biufc' else x)
    return dataframe
    