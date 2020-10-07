#import the pandas library
import pandas as pd

#open the email_refkey csv file
#open the census_gid csv file 
email_refkey = open('email_refkey_copy.csv')
census_gid = open('revised_census_gid.csv')

#save corresponding files into dataframes
email_df = pd.read_csv(email_refkey, sep = ',', dtype = {"NAMEGASB" : "string", "CENSUSID" : "string", "State" : "string", "NameID" : "string"})
census_gid_df = pd.read_csv(census_gid, sep = ',', dtype = {"CENSUS_ID" : "string", "NAME_GASB" : "string", "NAME_CENSUS" : "string", "STATE_NAME" : "string"})

#array of "NAMEGASB, STATE" combinations that span across distinct CENSUSID (INVALID)
namegasb_duplicates = []

#array of "NAMEGASB, STATE" combinations that have identical CENSUSID (VALID)
namegasb_valid = []

"""
#array of "NameID" values that span across distinct CENSUSID
nameid_duplicates = []
"""

#function that determines if an array of 
#census ID's contain more than one distinct ID
def duplicate_id(array):
    if(len(array) == 0):
        return False
    
    id = array[0]

    for i in array:
        if id != i:
            return True
    
    return False


#main function
#for each row in email_refkey, we will check to see
#if NAMEGASB is a duplicate
for ind in email_df.index:

    #if censusid is null, just continue to next index
    if pd.isna(email_df['CENSUSID'][ind]):
        continue
    
    #if NAMEGASB is null, just continue
    #For this project I only dealt with duplicates in instances
    #where NAMEGASB was not Null. 
    if pd.isna(email_df["NAMEGASB"][ind]):
        continue
        """
        nameID = email_df["NameID"][ind]
        temp_df = census_gid_df.loc[census_gid_df["NAME_CENSUS"] == nameID]
        print(temp_df)
        arr_of_censusid = temp_df["ï»¿CENSUS_ID"].tolist()

        if(duplicate_id(arr_of_censusid)):
            nameid_duplicates.append(nameID)
        """
    
    #if NAMEGASB isn't null, the code below executes. 

    #extract namegasb and state values from the row
    namegasb = email_df["NAMEGASB"][ind]
    state = email_df["State"][ind]

    if namegasb + ", " + state in namegasb_valid:
        continue
 
    if namegasb + ", " + state in namegasb_duplicates:
        email_df['CENSUSID'][ind] = 'NULL'
        continue
    

    temp_df1 = census_gid_df.loc[census_gid_df["NAME_GASB"] == namegasb]
    temp_df2 = temp_df1.loc[temp_df1["STATE_NAME"].str.upper() == state]

    array_of_censusid = temp_df2["ï»¿CENSUS_ID"].tolist()

    is_duplicate = duplicate_id(array_of_censusid)
    
    if(is_duplicate):
        email_df['CENSUSID'][ind] = 'NULL'
        namegasb_duplicates.append(namegasb + ", " + state)
    else:
        namegasb_valid.append(namegasb + ", " + state)
    


print(namegasb_duplicates)










