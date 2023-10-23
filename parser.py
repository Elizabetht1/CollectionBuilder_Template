#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import numpy as np

df_path:str = "/Users/elizabethterveen/Downloads/Black Archive.xlsx - Periodicals & Journals.xlsx - Table 1.csv"

def chunk(archive_data:pd.DataFrame) -> list:
    return list(archive_data[archive_data["Number"].isna() == False].index)

def condense_col(archive_data:pd.DataFrame,column:str,start_ind:int,end_ind:int)->str:
    col_str:str = ""
    s:int = start_ind
    e:int = end_ind
    while s <e:
        ##concat col_str with the next ind
        elem = archive_data.iloc[s][column]
        if elem is not np.nan:
            col_str = col_str +" "+ str(archive_data.iloc[s][column])
        s+=1 
    return col_str

def parse(archive_data:pd.DataFrame)->pd.DataFrame:
    chunk_inds:list = chunk(archive_data) #get inds of real values 
    chunk_inds.append(archive_data.index.stop) ##actual last index should be last row of df

    i:int = 1;

    parsed_data:list = [] #where we'll store new rows 
    cols:list = list(archive_data.columns) #list of data cols names

    while i < len(chunk_inds):

        start:int = chunk_inds[i-1] #initalize a chunk
        end:int= chunk_inds[i]

        new_row:list = list(archive_data.iloc[start]) #put the start row in new row 
        
        ##flatten all rows associated with this object into a single cell 
        for c in range(len(cols)) : 
            name = cols[c]; 
            col_str = condense_col(archive_data,name,start,end)
            if col_str != "":
                new_row[c] = col_str
            else:
                new_row[c] = None
        parsed_data.append(new_row)

        i+=1

    return pd.DataFrame(parsed_data,columns = cols)

def main():
    df:pd.DataFrame = pd.read_csv(df_path)
    parse(df)

if __name__ == "__main__":
    main()


