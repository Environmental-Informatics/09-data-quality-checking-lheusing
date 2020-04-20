#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 14:21:53 2020
@author: lheusing


check for gross errors, check for inconsistency in var, and check for range problems
make each check a function that returns n failed
summarize the results of the check and write clean data to quality csv
https://www.youtube.com/watch?v=vmEHCJofslg for help with pandas .iloc and .loc
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def ReadData( fileName ):
    """This function takes a filename as input, and returns a dataframe with
    raw data read from that file in a Pandas DataFrame.  The DataFrame index
    should be the year, month and day of the observation.  DataFrame headers
    should be "Date", "Precip", "Max Temp", "Min Temp", "Wind Speed". Function
    returns the completed DataFrame, and a dictionary designed to contain all 
    missing value counts."""
    
    # define column names
    colNames = ['Date','Precip','Max Temp', 'Min Temp','Wind Speed']

    # open and read the file
    DataDF = pd.read_csv("DataQualityChecking.txt",header=None, names=colNames,  
                         delimiter=r"\s+",parse_dates=[0])
    DataDF = DataDF.set_index('Date')

    
    
    # define and initialize the missing data dictionary
    ReplacedValuesDF = pd.DataFrame(0, index=["1. No Data"], columns=colNames[1:])
     
    return( DataDF, ReplacedValuesDF )
 
def Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF ):
    """This check replaces the defined No Data value with the NumPy NaN value
    so that further analysis does not use the No Data values.  Function returns
    the modified DataFrame and a count of No Data values replaced."""

    # check for -999 chagne to na
    DataDF.replace(-999, np.nan, inplace = True)
    
    #write sum of na to .loc of No data
    ReplacedValuesDF.loc['1. No Data',:] = DataDF.isna().sum()

    return( DataDF, ReplacedValuesDF )
    
def Check02_GrossErrors( DataDF, ReplacedValuesDF ):
    """This function checks for gross errors, values well outside the expected 
    range, and removes them from the dataset.  The function returns modified 
    DataFrames with data the has passed, and counts of data that have not 
    passed the check."""
 
    #dont know why this is failing. use .loc in future
    #filter1 =  DataDF.loc(DataDF['Precip']< 0) 
    #filter2 =  DataDF['Precip']<0 
   # DataDF['Precip'].where(filter1, other = np.nan, inplace = True)
    
    #check for gross eror via .loc and change to nan
    DataDF['Precip'].loc[(DataDF['Precip']>25) | (DataDF['Precip']<0)] = np.nan
    DataDF['Max Temp'].loc[(DataDF['Max Temp']>35) | (DataDF['Max Temp']<-25)] = np.nan
    DataDF['Min Temp'].loc[(DataDF['Min Temp']>35) | (DataDF['Min Temp']<-25)] = np.nan
    DataDF['Wind Speed'].loc[(DataDF['Wind Speed']>10) | (DataDF['Wind Speed']<0)] = np.nan
    
    #write sum of nans to replaced value while subtracting the old count of -999
    ReplacedValuesDF.loc['2. Gross Error',:] = DataDF.isna().sum() - ReplacedValuesDF.sum()
    return( DataDF, ReplacedValuesDF )
    
def Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture is less than
    minimum air temperature, and swaps the values when found.  The function 
    returns modified DataFrames with data that has been fixed, and with counts 
    of how many times the fix has been applied."""
 
    #create counter to keep track of swaps
    i = len(DataDF.loc[DataDF['Max Temp'] < DataDF['Min Temp']]) 
    ReplacedValuesDF.loc['3. Swapped',:] = [0, i , i ,0]
    
    #swap the data
    DataDF.loc[DataDF['Max Temp'] < DataDF['Min Temp'], ['Max Temp','Min Temp']]  = DataDF.loc[DataDF['Max Temp'] < DataDF['Min Temp'], ['Min Temp','Max Temp']] 
    

    return( DataDF, ReplacedValuesDF )
    
def Check04_TmaxTminRange( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture minus 
    minimum air temperature exceeds a maximum range, and replaces both values 
    with NaNs when found.  The function returns modified DataFrames with data 
    that has been checked, and with counts of how many days of data have been 
    removed through the process."""
    
    
    i = len(DataDF.loc[(DataDF['Max Temp'] - DataDF['Min Temp']) > 25])
    DataDF.loc[(DataDF['Max Temp'] - DataDF['Min Temp'] > 25) , ['Max Temp', 'Min Temp']] = np.nan
    
    #cant import i from before thus cant use
    #ReplacedValuesDF.loc['4. Range Fail',:] = DataDF.isna().sum() - ReplacedValuesDF.sum() + [0 , i , i ,0]

   # use to check  switches 
   #j = len(DataDF.loc[(DataDF['Max Temp'] - DataDF['Min Temp']) > 25])
    ReplacedValuesDF.loc['4. Range Fail',:] = [0 ,i ,i ,0 ]

    return( DataDF, ReplacedValuesDF )
    
def providerawdata(filename):
    """This function takes a filename as input, and returns a dataframe with
    raw data read from that file in a Pandas DataFrame.  The DataFrame index
    should be the year, month and day of the observation.  DataFrame headers
    should be "Date", "Precip", "Max Temp", "Min Temp", "Wind Speed". Function
    returns the completed DataFrame, and a dictionary designed to contain all 
    missing value counts. """
    
    # define column names
    colNames = ['Date','Precip','Max Temp', 'Min Temp','Wind Speed']

    # open and read the file
     
    DataDFraw = pd.read_csv("DataQualityChecking.txt",header=None,names=colNames,  
                         delimiter=r"\s+",parse_dates=[0])
    DataDFraw = DataDFraw.set_index('Date')
    
    
    return( DataDFraw)

# the following condition checks whether we are running as a script, in which 
# case run the test code, otherwise functions are being imported so do not.
# put the main routines from your code after this conditional check.

if __name__ == '__main__':

    fileName = "DataQualityChecking.txt"
    DataDF, ReplacedValuesDF = ReadData(fileName)
    
    print("\nRaw data.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF )
    
    print("\nMissing values removed.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check02_GrossErrors( DataDF, ReplacedValuesDF )
    
    print("\nCheck for gross errors complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF )
    
    print("\nCheck for swapped temperatures complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check04_TmaxTminRange( DataDF, ReplacedValuesDF )
    
    print("\nAll processing finished.....\n", DataDF.describe())
    print("\nFinal changed values counts.....\n", ReplacedValuesDF)
    

    DataDFraw = providerawdata(fileName) #provide raw data to plot against
    
    
    #precipitation plot
    plt.subplots(figsize = (8,5))
    
    plt.scatter(DataDF.index,DataDFraw.Precip, color = 'b', label = "Uncorrected Precip")
    plt.scatter(DataDF.index,DataDF.Precip, color = 'r', label = "Corrected Precip")
    
    plt.legend()
    plt.savefig('Precip.jpg')
    plt.show()
    plt.close()
    
    #Max temp plot
    fig, a = plt.subplots(figsize = (8,5))
    
    plt.scatter(DataDF.index,DataDFraw['Max Temp'], color = 'b', label = "Uncorrected max temp")
    plt.scatter(DataDF.index,DataDF['Max Temp'], color = 'r', label = "Corrected max temp")
    

    plt.legend()
    plt.savefig('max temp.jpg')
    plt.show()
    plt.close()
    
    #Min temp plot
    plt.subplots(figsize = (8,5))
    
    plt.scatter(DataDF.index,DataDFraw['Min Temp'], color = 'b', label = "Uncorrected min temp")
    plt.scatter(DataDF.index,DataDF['Min Temp'], color = 'r', label = "Corrected min temp")
    

    plt.legend()
    plt.savefig('min temp.jpg')
    plt.show()
    plt.close()
    
    #wind speed plot
    plt.subplots(figsize = (8,5))
    
    plt.scatter(DataDF.index,DataDFraw['Wind Speed'], color = 'b', label = "Uncorrected wind speed")
    plt.scatter(DataDF.index,DataDF['Wind Speed'], color = 'r', label = "Corrected wind speed")
    
    plt.legend()
    plt.savefig('wind speed.jpg')
    
    plt.show()
    plt.close()
    
    #save DF to csv and save replacement data to other csv
    
    DataDF.to_csv("Quality_data", sep = "\t")
    ReplacedValuesDF.to_csv("replacement_data_stats", sep = "\t")
    
