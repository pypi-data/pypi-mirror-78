
import warnings
import pingouin as pg
import pandas as pd
import researchpy
from scipy.stats import spearmanr

warnings.filterwarnings("ignore")
def process(df,table,ls,name,k):
    '''
    This function returns data frame which contains one way anova test on categorical and numerical column. 
    
    Parameters:
       df (Data Frame) : The DataFrame which is to be used for calculating one way anova test.
       ls : list of numerical columns.
       name : list of categorical columns.
       table : Empty data frame.
       k : looping parameters. 
    
    Returns:
       The DataFrame which contains spearman correlation coefficient and p value.
    
    '''
    if k==len(name):
        return table[table['p-unc']>0.05] 
    else:
        for item in ls:
            tab=pg.anova(dv=item,between=[name[k]],data=df)
            tab['col']=item
            table=tab.append(table)
        return process(df,table,ls,name,k+1)

def anov(df):
    lst=list(df.select_dtypes(include=['object']))
    ls=list(df.select_dtypes(exclude=['object']))
    table=pd.DataFrame()
    return process(df,table,ls,lst,0)
 


def val_return(df,lst,n,matrix):
    '''
    This function returns data frame which contains spearman correlation coefficient and p value of numerical data only. 
    
    Parameters:
       df (Data Frame) : The DataFrame which is to be used for calculating correlation coefficient and p value.
       lst : list of numerical columns.
       matrix : Empty data frame.
       n : looping parameters. 
    
    Returns:
       The DataFrame which contains spearman correlation coefficient and p value.
    
    '''
    if n==len(lst) or len(lst)==0:
        return matrix[(matrix['coef']>=0.7) | (matrix['coef']<=-0.7)]
    else:
        coef, p = spearmanr(df[lst[n-1]], df[lst[n]])
        matrix.loc[n-1]=[lst[n-1],lst[n],coef,p]
        return val_return(df,lst,n+1,matrix)
    
def correlation_coef(df):
    df=df.select_dtypes(exclude=["object_"])
    matrix=pd.DataFrame(columns=['Source','col','coef','p'])
    return val_return(df,list(df.columns),1,matrix) 




def chitest(df,lst,table,k,j):
    '''
    This function returns data frame which contains Chi-sqaure test of categorical data only. 
    
    Parameters:
       df (Data Frame) : The DataFrame which is to be used for calculating Chi-sqaure test.
       lst : list of categorical columns.
       table : Empty data frame.
       k and j : looping parameters. 
    
    Returns:
       The DataFrame which contains Chi-sqaure test of categorical data only.
    
    '''
    if k==len(lst):
        if j==len(lst):
            return table[table['results']>0.15]
        else:
            return chitest(df,lst,table,j+1,j+1)
    else:
        crosstab, res = researchpy.crosstab(df[lst[j-1]], df[lst[k]], test= "chi-square") 
        res['Source']=lst[j-1]
        res['col']=lst[k]
        table=table.append(res.loc[2],sort=True)
        return chitest(df,lst,table,k+1,j)

def cattest(df):
    lst=list(df.select_dtypes(include=['object']))
    table=pd.DataFrame()
    return chitest(df,lst,table,1,1)


def corr_summ(df):
    '''
    This function returns the columns which contains correlation and its statistical significance. As this method calculates statistical significance on continuous numerical to continuous numerical columns, continuous numerical to categorical column and categorical to categorical columns.
    
    Parameters:
       df (Data Frame) : The DataFrame which is to be used for calculating its correlated and statistical significance.
    
    Returns:
       The DataFrame containing name of columns which are statistically highly correlated to each other.
    
    '''
    tab=pd.DataFrame()
    ntn=correlation_coef(df)
    ctn=anov(df)
    ctc=cattest(df)
    tab=tab.append([ntn[['Source','col']],ctn[['Source','col']],ctc[['Source','col']]],ignore_index = True)
    return tab
    