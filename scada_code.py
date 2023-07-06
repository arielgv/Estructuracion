#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from datetime import datetime
import numpy as np


# # STATION 

# Description: This script takes in a file named Station.csv(default) , recognizes its information and interprets the columns. Finally prints and save a Dat format file with the predefined tables for further processing

# Station Data Conversion REFERENCE : 
# 
# ORDER : Padded with incremental index numbering
# 
# Key : Column "Name" in Station.csv  . Erased blank spaces.('Example_ _')
# 
# Name : Column "Desc" in Station.csv . Erased blank spaces.('Example_ _')
# 
# AOR : Column Zones in Station.csv. 

# The .str.rstrip() method is widely used since many fields (almost all of them) have their value ending with two blank spaces.

# In[5]:


#Input Filename (default = Station.csv)
InputStationFile = "Station.csv"


# In[6]:


df = pd.read_csv(InputStationFile, skipinitialspace=True)
df.columns = df.columns.str.strip()

df_output = pd.DataFrame()
df_output['Order'] = range(len(df)) # Order column was not  specified in documentation. So in default is a unique incremental index.
df_output['Key'] = '"'+ df['Name'].str.rstrip() + '"'  
df_output['Name'] = '"' + df['Desc'].str.rstrip() + '"' 
df_output['AOR'] = df['Zones']

#sorting
df_output = df_output[['Order', 'Key', 'Name', 'AOR']]
df_station = df_output

#verification
print(df_station)


# # Select Output name: (default: StationOutput.dat)

# In[1231]:


#Output:
stationfilename = "StationOutput.dat"


# In[1232]:


now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
with open(stationfilename, 'w') as f:
    f.write("*\n")
    f.write("****************************************************************\n")
    f.write(f"*  Creation Date/Time:  {now}\n")
    f.write("****************************************************************\n")
    f.write("*             Order  Key             Name                AOR\n")
    f.write("*             ----  -----   --------------------------   ---\n")
    f.write("*  2 STATION   0     3             4                      13\n")
    f.write("*---------------------------------------------------------------\n")

    for index, row in df_station.iterrows():
        f.write("{:<5}{:<5}{:<5}{:<5}{:<8}{:<30}{:<6}\n".format
                ("", row['Order'],"", row['Order'], row['Key'], row['Name'], row['AOR']))


# # END STATION

# --------------------------------------------------

# # STATUS

# Description: This script takes in a file named Status.csv(default) , recognizes its information and interprets the columns. Finally prints and save a Dat format file with the predefined tables for further processing

# Station Data Conversion REFERENCE : 
# 
# (1)Type : ( 
#        
#             If column "Telem_A" in status.csv = empty. C_IND.   Type = 5
# 
#             If column "Telem_A" in status.csv = any number. T_IND.  Type = 1
#             
#             If column "Open_B" in status.csv = 12.  T_I&C.     Type = 2  ) 
#                 Criteria: only 42 rows (0,49%) has Open_B= 12.
#                         so its gonna be Type = 2 regardless the value of Telem_A, 
#                         giving priority to Open_B.
#                         (In evey case of Open_B=12, Telem_A showed a number also)
#               
#               Edited:  IF column Stn = 054 (PS. PSEUDO POINTS) , M_IND. Type = 8 
# 
# (3)Key : Format XXYYYZZZ
#                          XX =   If type (descripted before) = 1 , XX = 01
#                                 If type (descripted before) = 2 , XX = 01
#                                 If type (descripted before) = 5 , XX = 02
#                                 If type (descripted before) = 8 , XX = 12
#                          YYY = Stn (Station Order number.)(descripted in this Markdown)
#                          ZZZ = Incremental number per station
# 
# (4)Name : Column "Name" + column "Desc" in Status.csv. Replace the commas (,) with blank spaces.
# 
# (5) Stn : (XXX) -> The first characters of the "Name" column in the current dataset, before the comma (,), reference the value of the KEY column in the previous dataset (Station). This value is based on the Order column. This number should be expressed in three digits (e.g., 38 = 038).
# 
# (10) Aor : Column "Zones" in Status.csv
# 
# (19) pState : Column "Presuffx" in Status.csv
# 
# (49) Norm : Column "Normal_State" in Status.csv
# 
# (29) AlarmGroup: Will be set to 1 unless defined in mapping document
# 
# (41) ICAddress : Refer to documentation. This script leaves it in blank

# In[1233]:


#Input filename(default: "Status.csv")
InputStatusFile = "Status.csv"


# In[1234]:


status_df = pd.read_csv(InputStatusFile)
df_status = pd.DataFrame()


# In[1235]:


df_status['Type'] = np.where(status_df['Open_B  '] == '12  ', 2, np.where(status_df['Telem_A  '].replace('  ', np.nan).notna(), 1, 5))
df_status['Name'] = status_df['Name  '].str.replace(',',' ') + " " + status_df['Desc  ']
df_status['Name'] = df_status['Name'].str.rstrip()
df_status['AOR'] = status_df['Zones  '].str.rstrip()
df_status['pState'] = status_df['PreSuffx  ']
df_status['Norm'] = status_df['Normal_State  ']
df_status['AlarmGroup'] = 1
df_status['ICAddress'] = np.nan


# In[1236]:


df_status


# # Stn :

# This code strips the Name column in status and search the matching row Key in Station Dataframe
# then, it reads the Order column value and assign this to the Stn column

# In[1237]:


status_df['Key'] = status_df['Name  '].str.split(',').str[0].str.strip()  # make sure no blank spaces are in the begin & end of the name
df_station['Key'] = df_station['Key'].str.replace('"', '')
stn_values = []  #list for store stn values


# In[1238]:


for i in range(len(status_df)):
    matching_row = df_station[df_station['Key'] == status_df.loc[i, 'Key']]
    if not matching_row.empty:
        stn_values.append(f"{matching_row['Order'].values[0]:03}")
    else:
        stn_values.append(np.nan)
df_status['Stn'] = stn_values


# In[1239]:


df_status


# Replacement case: Pseudo Points.
# IF stn = 054 (PS. Pseudo points.) Set type to 8 .   And then set XX Value to 12

# In[1240]:


df_status.loc[df_status['Name'].str.startswith("PS"), 'Type'] = 8

for i in range(len(df_status)):
    if df_status.loc[i, 'Stn'] == '054':
        key_to_search = df_status.loc[i, 'Name'][3:5]

        # Buscar valor 
        matching_row = df_station[df_station['Key'] == key_to_search]

        # != una fila correspondiente, 'Stn' en 'df_status'
        if not matching_row.empty:
            df_status.loc[i, 'Stn'] = f"{matching_row['Order'].values[0]:03}"


# # KEY

# In[1241]:


key_values = []
xx_yyy_counters = {}  # creating a dict to store and count every YYY. It's used for a incremental ZZZ


# In[1242]:


for i in range(len(df_status)):
    
    if df_status.loc[i, 'Type'] == 1:
        xx = '01'
    elif df_status.loc[i, 'Type'] == 2:
        xx = '01'
    elif df_status.loc[i, 'Type'] == 5:
        xx = '05'
    elif df_status.loc[i, 'Type'] == 8:
        xx = '12'
    else:
        xx = '99'  # ERROR CASE . In case of being unable to find a coincidence.

    yyy = df_status.loc[i, 'Stn']

    # combination
    key = xx + yyy

    # if key exists in counters, then add +1 , else, initialites it.
    if key in xx_yyy_counters:
        xx_yyy_counters[key] += 1
    else:
        xx_yyy_counters[key] = 1

    #   Current Value of ZZZ . 
    zz = f"{xx_yyy_counters[key]:03}"  #03 (Default). the number of Z in the format (default XX YYY ZZZ (3 Z))

    key_values.append(xx + yyy + zz)


# In[1243]:


df_status['Key'] = key_values


# In[1244]:


#obtaining and showing the counting of Types.
type_counts = df_status['Type'].value_counts()
print(type_counts)


# In[1245]:


new_order = ['Type','Key','Name','Stn','AOR','pState','Norm','AlarmGroup','ICAddress']
df_status = df_status[new_order]


# In[1246]:


df_status


# # DATASET Status ready.

# # OUTPUT TO DAT FILE :

# In[1247]:


output_status_name = 'StatusOutput.dat'


# In[1248]:


#Width definition. 
indent_format = "{:<10}"  # Initial TAB
indent2 = "{:1}"
type_format = "{:<6}"
key_format = "{:<8}"
name_format = "{:<37}"
stn_format = "{:<6}"
aor_format = "{:<16}"
pstate_format = "{:<9}"
norm_format = "{:<7}"
alarmgroup_format = "{:<13}"
icaddress_format = "{:<20}"


with open(output_status_name, 'w') as f:
    f.write('*         Type  Key          Name                                      Stn   AOR               pState   Norm   AlarmGroup   ICAddress\n')
    f.write('*         ----  ---          ----                                      ---   ---               ------   ----   ----------   ---------\n')
    f.write('4 STATUS  (1)   (3)          (4)                                       (5)   (10)              (19)     (49)   (29)         (41)\n')

    for i in range(len(df_status)):
        f.write(indent_format.format('') + 
                type_format.format(df_status.loc[i, 'Type']) +
                "\"" + key_format.format(df_status.loc[i, 'Key']) + "\"" +
                indent2.format('') + 
                indent2.format('') + 
                indent2.format('') + 
                "\"" + name_format.format(df_status.loc[i, 'Name']) + "\"" +
                indent2.format('')+
                indent2.format('') + 
                indent2.format('') + 
                stn_format.format(df_status.loc[i, 'Stn']) +
                aor_format.format(df_status.loc[i, 'AOR']) + 
                indent2.format('')+
                indent2.format('') + 
                pstate_format.format(df_status.loc[i, 'pState']) +
                norm_format.format(df_status.loc[i, 'Norm']) +
                alarmgroup_format.format(df_status.loc[i, 'AlarmGroup']) +
                icaddress_format.format(df_status.loc[i, 'ICAddress']) + '\n')


# # END STATUS

# -------------------------------

# # ANALOG

# Description: This script takes in a file named Analog.csv(default) , recognizes its information and interprets the columns. Finally prints and save a Dat format file with the predefined tables for further processing

# ANALOG Data conversion REFERENCE :
# 
#  Type (1) :  Columns : 
#  
#                         IF Telem_B  !=  21  . T_ANLG  = type : 1
# 
#                         IF Telem_RTU = blank .   C_ANLG =  Type : 2
# 
#                         IF NOT Defined. Manual = Type: 3 
# 
#                         * CRITERIA: 100% of the Telem_B column is different from 21, while 40% of the Telem_RTU column is blank. To prioritize visibility of Telem_RTU in case of conflict, the priority will be given to C_ANLG (Type 2).
# 
# Key (3)   :  XX YYY ZZZ
# 
# Name (4)  :  Columns : Name + Desc . 
#                 If not defined, set to KEY 
# 
# Stn (5)   :  ###  -> The first characters of the "Name" column in the current dataset, before the comma (,), reference the value of the KEY column in the Station dataset. This value has a number based on the Order column. This number should be expressed in three digits (e.g., 38 = 038).
# 
# AOR (10)  :   Column Zones in Analog.csv
# 
# pScale (24): Column EU_HI in Analog.csv
# 
# AlarmGrp  (42)  :  Set to default: 1
# 
# ICAddress (66)  : It will be declared as NaN.
# 
# NominalHiLimits (77,4):  column Alm_unrHi in Analog.csv , named in this df:  Nominal_HiLim
#  *Edited:  NominalHiLimits (77:4): RENAMED TO HiLim[1]  (Rsnblty)
# 
# NominalLowLimits (78,4):  column Alm_unrLo in Analog.csv  , named in this df: Nominal_LoLim
#  *Edited: RENAMED TO LoLim[1]   (Rsnblty)
# 
#  ADDED:NominalHiLimits (77:0-3): Column Alm_preHi in Analog.csv, named in this df: HiLim[0]    (High)
#  ADDED:NominalLowLimits (78:0-3): Colum Aim_preLo in Analog.csv, named in this df: LoLim[0]    (Low)
#  
#     
#    

# In[7]:


#Data CSV Name entry
analog_file = "Analog.csv"


# In[8]:


df_analog = pd.read_csv(analog_file)

df_new = pd.DataFrame()


conditions = [
    (df_analog['Telem_RTU  '] == "  "),
    (df_analog['Telem_B  '] != "21  ")
]
choices = [1, 2]
df_new['Type'] = np.select(conditions, choices, default=3)

df_new['Name'] = df_analog['Name  '].str.replace(',',' ') + " " + df_analog['Desc  ']
df_new['AOR'] = df_analog['Zones  ']
df_new['AlarmGrp'] = 1
df_new['ICAddress'] = "NaN"
df_new['Nominal_HiLim'] = df_analog['Alm_unrHi  '] #HiLim[0] -> Rsnblty
df_new['Nominal_LoLim'] = df_analog['Alm_unrLo  '] #LoLim[0] -> Rsnblty

#edited
#----
df_new['Nominal_HiLim1'] = df_analog['Alm_preHi  '] #HiLim[1] -> High
df_new['Nominal_LoLim1'] = df_analog['Alm_preLo  '] #LoLim[1] -> Low
#----

def keep_decimal_precision(val):
    try:
        float_val = float(val)
        if float_val.is_integer():
            return str(int(float_val))
        else:
            return str(float_val)
    except ValueError:
        return val

df_analog['EU_Hi  '] = df_analog['EU_Hi  '].apply(keep_decimal_precision)
df_new['pScale EU_Hi'] = df_analog['EU_Hi  ']



# # STN 

# In[9]:


df_analog['Key'] = df_analog['Name  '].str.split(',').str[0].str.strip()

stn_values = []

for i in range(len(df_analog)):
    
    matching_row = df_station[df_station['Key'] == df_analog.loc[i, 'Key']]
    
    if not matching_row.empty:
        stn_values.append(f"{matching_row['Order'].values[0]:03}")
    else:
        stn_values.append(np.nan)
df_new['Stn'] = stn_values


# In[10]:


df_new


# # KEY

# In[11]:


key_values = []
xx_yyy_counters = {}


# In[12]:


for i in range(len(df_new)):
    
    # Asignamos el valor correspondiente a 'XX' según el valor de 'Type'
    if df_new.loc[i, 'Type'] == 1:
        xx = '03'
    elif df_new.loc[i, 'Type'] == 2:
        xx = '04'
    else:
        xx = '99'  # ERROR CASE


    yyy = str(df_new.loc[i, 'Stn'])

    key = xx + yyy

    if key in xx_yyy_counters:
        xx_yyy_counters[key] += 1
    else:
        xx_yyy_counters[key] = 1

    zz = f"{xx_yyy_counters[key]:03}"

    key_values.append(xx + yyy + zz)

df_new['Key'] = key_values


# In[13]:


df_new


# In[14]:


df_new = df_new[['Type', 'Key', 'Name', 'Stn', 'AOR', 'Nominal_HiLim', 'Nominal_HiLim1', 'Nominal_LoLim', 'Nominal_LoLim1', 'pScale EU_Hi', 'AlarmGrp']].copy()
df_new['ICAddress'] = "NaN"


# In[15]:


df_new


# Output Filename:

# In[16]:


output_analog_name = 'AnalogOutput.dat'


# In[37]:


indent_format = "{:<10}" 
indent2 = "{:1}"
type_format = "{:<6}"
key_format = "{:<8}"
name_format = "{:<41}"
stn_format = "{:<6}"
aor_format = "{:<17}"
nominal_hilim_format = "{:<16}"
nominal_hilim1_format = "{:<16}"
nominal_lolim_format = "{:<19}"
nominal_lolim1_format = "{:<12}"
alarmgroup_format = "{:<13}"
icaddress_format = "{:<20}"
pscale_format = "{:<15}"
eu_hi_format = "{:<20}"

with open(output_analog_name, 'w') as f:
   
    f.write('*         Type  Key          Name                                          Stn   AOR                HiLim[0](High)   HiLim[1](Rsnblty)  LoLim[0](Low)   LoLim[1](Rsnblty)  AlarmGroup   pScale(EU_Hi)  ICAddress\n')
    f.write('*         ----  ---          ----                                          ---   ---                --------------   -----------------  -------------   -----------------  ----------   -------------  ---------\n')
    f.write('5 ANALOG  (1)   (3)          (4)                                           (5)   (10)               (77,0)           (77,4)             (78,0)          (78,4)             (42)         (24)           (66)\n')

    
    for i in range(len(df_new)):
        f.write(indent_format.format('') + 
                type_format.format(str(df_new.loc[i, 'Type'])) +
                "\"" + key_format.format(df_new.loc[i, 'Key']) + "\"" +
                indent2.format('') + 
                indent2.format('') + 
                indent2.format('') + 
                "\"" + name_format.format(df_new.loc[i, 'Name']) + "\"" +
                indent2.format('')+
                indent2.format('') + 
                indent2.format('') + 
                stn_format.format(str(df_new.loc[i, 'Stn'])) +
                aor_format.format(str(df_new.loc[i, 'AOR'])) + 
                indent2.format('')+
                indent2.format('') + 
                nominal_hilim1_format.format(str(df_new.loc[i, 'Nominal_HiLim1']))+
                indent2.format('')+
                nominal_hilim_format.format(str(df_new.loc[i, 'Nominal_HiLim'])) +
                indent2.format('')+
                indent2.format('')+
                indent2.format('')+
                nominal_lolim1_format.format(str(df_new.loc[i, 'Nominal_LoLim1']))+
                
                indent2.format('')+
                indent2.format('')+
                indent2.format('')+
                indent2.format('')+
                nominal_lolim_format.format(str(df_new.loc[i, 'Nominal_LoLim'])) +

                alarmgroup_format.format(str(df_new.loc[i, 'AlarmGrp'])) +
                pscale_format.format(df_new.loc[i, 'pScale EU_Hi']) +
               
                icaddress_format.format(df_new.loc[i, 'ICAddress']) + '\n')


# In[ ]:




