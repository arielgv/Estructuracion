#!/usr/bin/env python
# coding: utf-8

# In[103]:


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

# In[177]:


#Input Filename (default = Station.csv)
InputStationFile = "Station.csv"


# In[178]:


df = pd.read_csv(InputStationFile, skipinitialspace=True)
df.columns = df.columns.str.strip()

df_output = pd.DataFrame()
df_output['Order'] = range(1, len(df)+1) # Order column was not  specified in documentation. So in default is a unique incremental index.
df_output['Key'] = '"'+ df['Name'].str.rstrip() + '"'  
df_output['Name'] = '"' + df['Desc'].str.rstrip() + '"' 
df_output['AOR'] = df['Zones']

#sorting
df_output = df_output[['Order', 'Key', 'Name', 'AOR']]
df_station = df_output

#verification
print(df_station)


# # Select Output name: (default: StationOutput.dat)

# In[179]:


#Output:
stationfilename = "Station99.dat"


# In[180]:


now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
with open(stationfilename, 'w') as f:
    f.write("*\n")
    f.write("****************************************************************\n")
    f.write(f"*  Creation Date/Time:  {now}\n")
    f.write("****************************************************************\n")
    f.write("*             Order  Key             Name                AOR\n")
    f.write("*             ----  -----   --------------------------   ---\n")
    f.write("\t2\tSTATION\t0\t3\t4\t13\n")
    f.write("*---------------------------------------------------------------\n")

    for index, row in df_station.iterrows():
        f.write("{}\t{}\t{}\t{}\t{}\t{}\n".format
                ("", row['Order'], row['Order'], row['Key'], row['Name'], row['AOR']))
    f.write(" 0")  


# # END STATION

# --------------------------------------------------

# # DEVICE_INSTANCE

# Description: This script takes in a file named STATUS.csv , uses a column named 'NAME'
# Instruction : Remove the first three characters so only the text after the comma remains. Then delete repetitions . From the 5000 records we should end with about 3800. 

# Desired output:
# 
# */             Order  Name
# */             ----  -----      
# 	53	DEVICE_INSTANCE	0
# *---------------------------------------------------------------
# 	1	"MTXTOT"
# 	2	"DRD"
# 	3	"35C109"  

# In[108]:


df_device_instance = pd.read_csv('Status.csv')


# In[109]:


df_device_instance = df_device_instance[['Name  ']]


# In[110]:


df_device_instance['Name  '] = df_device_instance['Name  '].str[3:]


# In[92]:


df_device_instance = df_device_instance.drop_duplicates()


# In[111]:


df_device_instance


# In[112]:


df_device_instance['Number'] = range(1,len(df_device_instance)+1)


# In[113]:


df_device_instance = df_device_instance[['Number', 'Name  ']]


# In[114]:


df_device_instance


# In[115]:


df_analog_instance = pd.read_csv('Analog.csv')

df_analog_instance = df_analog_instance[['Name  ']]
df_analog_instance['Name  '] = df_analog_instance['Name  '].str[3:]
df_analog_instance = df_analog_instance.drop_duplicates()

# Concatenar los DataFrames df_device_instance y df_analog_instance
result_df = pd.concat([df_device_instance, df_analog_instance], ignore_index=True)
result_df.drop_duplicates(subset='Name  ', inplace=True, keep='first')

# Mostrar el DataFrame resultante
print(result_df)


# In[ ]:





# In[116]:


df_device_instance = result_df


# In[117]:


df_device_instance['Number'] = range(1,len(df_device_instance)+1)


# In[118]:


df_device_instance


# In[119]:


df_device_instance['Name  '] = df_device_instance['Name  '].str.rstrip() 


# In[120]:


with open('Device_instance.dat', 'w') as f:
    f.write("*\n")
    f.write("*\n")
    f.write("*\n")
    f.write("\t53\tDEVICE_INSTANCE\t0\n")
    f.write("*--Index---Name----------------------------------\n")

    for index, row in df_device_instance.iterrows():
        f.write("\t{}\t{}\n".format(index + 1, row['Name  ']))
    
    f.write(" 0")


# _________

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
#       *****
#        Updated : 2019-03-06 . (4) Name : Column "Desc" in Status.csv . If not defined will be set to Key 
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
# 
# * ***UPDATE : 
# (107) pDeviceInstance : Column "Name" in Status.csv . Get the string after the comma, then search for the matching record of the objet DEVICE_INSTANCE. 
# 

# In[121]:


#Input filename(default: "Status.csv")
InputStatusFile = "Status.csv"


# In[122]:


status_df = pd.read_csv(InputStatusFile)
df_status = pd.DataFrame()


# In[123]:


df_status['record'] = range(1, len(status_df)+1) 
df_status['OrderNo'] = range(1, len(status_df)+1) 


df_status['Type'] = np.where(status_df['Open_B  '] == '12  ', 2, np.where(status_df['Telem_A  '].replace('  ', np.nan).notna(), 1, 5))
#df_status['Name'] = status_df['Name  '].str.replace(',',' ') + " " + status_df['Desc  ']
#df_status['Name'] = df_status['Name'].str.rstrip()
df_status['Name'] = status_df['Desc  ']
df_status['AOR'] = status_df['Zones  '].str.rstrip()
df_status['pState'] = status_df['PreSuffx  ']
df_status['Norm'] = status_df['Normal_State  ']
df_status['AlarmGroup'] = 1
df_status['ICAddress'] = np.nan


# In[124]:


df_status


# In[126]:


df_device_instance


# In[127]:


status_df


# In[ ]:





# In[128]:


df_status['TempName'] = status_df['Name  '].str[3:]

# Elimina espacios en blanco al final de la columna temporal
df_status['TempName'] = df_status['TempName'].str.rstrip()

# Realiza la asignación de números basada en el nombre temporal
df_status['pDeviceInstance'] = df_status['TempName'].map(df_device_instance.set_index('Name  ')['Number'])

# Borra la columna temporal
df_status.drop(columns=['TempName'], inplace=True)

# Muestra el DataFrame resultante con la nueva columna
print(df_status)



# # Stn :

# This code strips the Name column in status and search the matching row Key in Station Dataframe
# then, it reads the Order column value and assign this to the Stn column

# In[129]:


status_df['Key'] = status_df['Name  '].str.split(',').str[0].str.strip()  # make sure no blank spaces are in the begin & end of the name
df_station['Key'] = df_station['Key'].str.replace('"', '')
stn_values = []  #list for store stn values


# In[130]:


for i in range(len(status_df)):
    matching_row = df_station[df_station['Key'] == status_df.loc[i, 'Key']]
    if not matching_row.empty:
        stn_values.append(f"{matching_row['Order'].values[0]:03}")
    else:
        stn_values.append(np.nan)
df_status['Stn'] = stn_values


# In[131]:


df_status


# Replacement case: Pseudo Points.
# IF stn = 054 (PS. Pseudo points.) Set type to 8 .   And then set XX Value to 12

# In[132]:


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

# In[133]:


key_values = []
xx_yyy_counters = {}  # creating a dict to store and count every YYY. It's used for a incremental ZZZ


# In[134]:


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


# In[135]:


df_status['Key'] = key_values


# In[136]:


#obtaining and showing the counting of Types.
type_counts = df_status['Type'].value_counts()
print(type_counts)


# In[137]:


df_status


# In[138]:


new_order = ['record', 'OrderNo','Type','Key','Name','Stn','AOR','pState','Norm','AlarmGroup','ICAddress','pDeviceInstance']
df_status = df_status[new_order]


# In[139]:


df_status


# In[140]:


df_status['Key'] = '"'+ df_status['Key'].str.rstrip() + '"'


# In[141]:


df_status['Name'] = '"'+ df_status['Name'].str.rstrip() + '"'


# In[142]:


df_status


# # DATASET Status ready.

# # OUTPUT TO DAT FILE :

# In[143]:


output_status_name = 'Status99.dat'


# In[144]:


with open(output_status_name, 'w') as f:
    f.write('* \n')
    f.write('\t4\tSTATUS\t0\t0\t1\t3\t4\t10\t19\t49\t29\t41\t107\n')
    f.write('*  record OrderNo   Type  Key          Name                                      Stn   AOR               pState   Norm   AlarmGroup   ICAddress   pDeviceInstance\n')

    for index, row in df_status.iterrows():
        f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format
                ("", row['record'], row['OrderNo'], row['Type'], row['Key'], row['Name'], row['Stn'], row['AOR'], row['pState'], row['Norm'], row['AlarmGroup'], row['ICAddress'], row['pDeviceInstance']))
    f.write(" 0")  


# In[145]:


OLD_CODE = """
#Width definition. 
tabspace = "{}/t"
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
                icaddress_format.format(df_status.loc[i, 'ICAddress']) + '\n') """


# # END STATUS

# -------------------------------

# # ANALOG

# Description: This script takes in a file named Analog.csv(default) , recognizes its information and interprets the columns. Finally prints and save a Dat format file with the predefined tables for further processing

# ANALOG Data conversion REFERENCE :
# 
#  Type (1) :  Columns : 
#  ///
#  
#             IF Telem_B  !=  21  . T_ANLG  = type : 1
# 
#         IF Telem_RTU = blank .   C_ANLG =  Type : 2
# 
#         IF NOT Defined. Manual = Type: 3 
# 
# * CRITERIA: 100% of the Telem_B column is different from 21, while 40% of the Telem_RTU column is blank. To prioritize visibility of Telem_RTU in case of conflict, the priority will be given to C_ANLG (Type 2).
#     ///
# 
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
# ______________________________________
# NominalHiLimits (77,1)
# 
# NominalHiLimits (77,2)
# 
# NominalHiLimits (77,3)
# 
# NominalHiLimits (77,4):  column * Alm_unrHi * in Analog.csv , named in this df:  Nominal_HiLim
# 
#  *Edited:  NominalHiLimits (77,4): RENAMED TO HiLim[1]  (Rsnblty)
# 
# NominalLowLimits (78,1)
# 
# NominalLowLimits (78,2)
# 
# NominalLowLimits (78,3)
# 
# NominalLowLimits (78,4):  column Alm_unrLo in Analog.csv  , named in this df: Nominal_LoLim
# 
#  *Edited: RENAMED TO LoLim[1]   (Rsnblty)
# 
#  ADDED:NominalHiLimits (77,0): Column Alm_preHi in Analog.csv, named in this df: HiLim[0]    (High)
# 
#  ADDED:NominalLowLimits (78,0): Colum Alm_preLo in Analog.csv, named in this df: LoLim[0]    (Low)
#  
# 
#  RG 9/14: There are three cases. 
# 
# 1. Hi limits are present but Lo are empty
# 
# If Alm_preHi, Alm_emgHi, Alm_unrHi have values but  Alm_preLo, Alm_emgLo, Alm_unrLo  are empty then set 78,0 to -99995 , 78,1 to -99996, 78,4 to -99999  and follow cells H89 and H90
# 
# 2. Lo limits are present but Hi are empty
# 
# If Alm_preLo, Alm_emgLo, Alm_unrLo have values but Alm_preHi, Alm_emgHi, Alm_unrHi are empty then set 77,0 to 99995 , 77,1 to 99996, 77,4 to 99999  and follow cells H91 and H92
# 
# 3. Hi and Lo limits are present. 
# 
# Follow indications of column H89, H90, H91 and H92
# Put the actual values presents.
# 
# 4. Hi and Lo are empty. Set 77,4 to 999999 and 78,4 -999999 , set 77,1 and 77,2 and 78,1 and 78,2 to 0.
# 
# 
# _____________________________________
# 
# NominalPairInactive (91) : RG 9/14: For cases 1,2 and 3 of cell I89 set to 0 the 91,1 and 91,2 and 91,3  , and set to 1 the  91,4 and 91,5 .
# 
# 91,1 91,2 91,3 . 91,4 91,5 
# 
# 
#     
#    

# In[146]:


#Data CSV Name entry
analog_file = "Analog.csv"


# las condiciones para el llenado de las columnas son las siguientes :
# 
# 1. Hi limits are present but Lo are empty:
# 
# If 'Alm_preHi  ', 'Alm_emgHi  ', 'Alm_unrHi  '(columnas encontradas dentro de df_analog)  have values but  'Alm_preLo  ', 'Alm_emgLo  ', 'Alm_unrLo  '(columnas encontradas dentro de df_analog)  are empty , then set Alm_preLo (de df_new) to -99995 , 78,1(crear esta columna) to -99996, 78,4(crear esta columna) to -99999  
# 
# Condicion 2:
# 2. Lo limits are present but Hi are empty
# 
# If 'Alm_preLo  ', 'Alm_emgLo  ', 'Alm_unrLo  '(columnas de df_analog)  have values but 'Alm_preHi  ', 'Alm_emgHi  ', 'Alm_unrHi  ' are empty then set Alm_preHi(de df_new) to 99995 , 77,1(crear esta columna) to 99996, 77,4(crear esta columna ) to 99999 
# 
# Condicion 3:
# 3. Hi and Lo limits are present. 
# 
# Tomar los valores presentes en df_analog para las columnas 'Alm_preHi  ', 'Alm_unrHi  ' y 'Alm_preLo  ', 'Alm_unrLo  ' y asignarlos a las columnas 'Alm_preHi', 'Alm_unrHi' y 'Alm_preLo', 'Alm_unrLo' de df_new.
# 
# 
# 

# In[147]:


df_analog = pd.read_csv(analog_file)

df_new = pd.DataFrame()
df_new['record'] = range(1, len(df_analog)+1) 
df_new['OrderNo'] = range(1, len(df_analog)+1) 

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


#df_new['Nominal_HiLim'] = df_analog['Alm_unrHi  '] #HiLim[0] -> Rsnblty
#df_new['Nominal_LoLim'] = df_analog['Alm_unrLo  '] #LoLim[0] -> Rsnblty

#edited
#----
#df_new['Nominal_HiLim1'] = df_analog['Alm_preHi  '] #HiLim[1] -> High
#df_new['Nominal_LoLim1'] = df_analog['Alm_preLo  '] #LoLim[1] -> Low
############
############



# HI LOW LIMITS

# In[148]:


for col in ['77,0', '77,1', '77,2', '77,3', '77,4', '78,0', '78,1', '78,2', '78,3', '78,4']:
    df_new[col] = 0  

for col in ['91,1', '91,2', '91,3', '91,4', '91,5']:
    df_new[col] = np.nan

# Condición 1:
mask1 = (
    df_analog[['Alm_preHi  ', 'Alm_emgHi  ', 'Alm_unrHi  ']].notna().any(axis=1) &
    df_analog[['Alm_preLo  ', 'Alm_emgLo  ', 'Alm_unrLo  ']].isin(["0  ", "  "]).all(axis=1)
)
df_new.loc[mask1, '78,0'] = -99995
df_new.loc[mask1, '78,1'] = -99996
df_new.loc[mask1, '78,4'] = -99999
df_new.loc[mask1, ['91,1', '91,2', '91,3']] = 0
df_new.loc[mask1, ['91,4', '91,5']] = 1


# Condición 2:
mask2 = (
    df_analog[['Alm_preLo  ', 'Alm_emgLo  ', 'Alm_unrLo  ']].notna().any(axis=1) &
    df_analog[['Alm_preHi  ', 'Alm_emgHi  ', 'Alm_unrHi  ']].isin(["0  ", "  "]).all(axis=1)
)
df_new.loc[mask2, '77,0'] = 99995
df_new.loc[mask2, '77,1'] = 99996
df_new.loc[mask2, '77,4'] = 99999
df_new.loc[mask2, ['91,1', '91,2', '91,3']] = 0
df_new.loc[mask2, ['91,4', '91,5']] = 1


# Condición 3:
df_new['77,0'] = df_analog['Alm_preHi  ']
df_new['77,4'] = df_analog['Alm_unrHi  ']
df_new['78,1'] = df_analog['Alm_emgLo  ']
df_new['78,4'] = df_analog['Alm_unrLo  ']
df_new.loc[df_new['77,0'].notna() | df_new['78,1'].notna(), ['91,1', '91,2', '91,3']] = 0
df_new.loc[df_new['77,0'].notna() | df_new['78,1'].notna(), ['91,4', '91,5']] = 1


# Condición 4:
mask4 = (
    df_analog[['Alm_preHi  ', 'Alm_emgHi  ', 'Alm_unrHi  ', 'Alm_preLo  ', 'Alm_emgLo  ', 'Alm_unrLo  ']].isin(["0  ", "  "]).all(axis=1)
)
df_new.loc[mask4, '77,4'] = 999999
df_new.loc[mask4, '78,4'] = -999999
df_new.loc[mask4, ['77,1', '77,2', '78,1', '78,2']] = 0


# In[149]:


df_new


# In[150]:


NOT_USED = """
# Convierte a float, convirtiendo errores a NaN
df_copy = df_analog.copy()

# Función para convertir '0  ' o '  ' en 0
def convert_zero(val):
    return 0 if val == '0  ' or val == '  ' else val

# Aplicar la función a todo el DataFrame
df_copy = df_copy.applymap(convert_zero)

# Convierte a float, convirtiendo errores a NaN
df_copy['Alm_unrHi  '] = pd.to_numeric(df_copy['Alm_unrHi  '], errors='coerce')
df_copy['Alm_unrLo  '] = pd.to_numeric(df_copy['Alm_unrLo  '], errors='coerce')
df_copy['Alm_preHi  '] = pd.to_numeric(df_copy['Alm_preHi  '], errors='coerce')
df_copy['Alm_preLo  '] = pd.to_numeric(df_copy['Alm_preLo  '], errors='coerce')

# Luego reemplaza los valores basados en las condiciones
df_copy.loc[df_copy['Alm_unrHi  '] == 0.0, 'Alm_unrHi  '] = 999999.0
df_copy.loc[df_copy['Alm_unrLo  '] == 0.0, 'Alm_unrLo  '] = -999999.0

# Para Alm_preHi y Alm_preLo, necesitamos considerar dos condiciones:
df_copy.loc[(df_copy['Alm_unrLo  '].notna()) & (df_copy['Alm_unrLo  '] != -999999.0), 'Alm_preHi  '] = 999998.0
df_copy.loc[(df_copy['Alm_unrHi  '].notna()) & (df_copy['Alm_unrHi  '] != 999999.0), 'Alm_preLo  '] = -999998.0


df_new['Nominal_HiLim'] = df_copy['Alm_unrHi  '] 
df_new['Nominal_LoLim'] = df_copy['Alm_unrLo  ']
df_new['Nominal_HiLim1'] = df_copy['Alm_preHi  '] 
df_new['Nominal_LoLim1'] = df_copy['Alm_preLo  ']
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

df_copy['Alm_unrHi  '] = df_copy['Alm_unrHi  '].apply(keep_decimal_precision)
df_copy['Alm_unrLo  '] = df_copy['Alm_unrLo  '].apply(keep_decimal_precision)
df_copy['Alm_preHi  '] = df_copy['Alm_preHi  '].apply(keep_decimal_precision)
df_copy['Alm_preLo  '] = df_copy['Alm_preLo  '].apply(keep_decimal_precision)


df_new['Nominal_HiLim'] = df_copy['Alm_unrHi  '] 
df_new['Nominal_LoLim'] = df_copy['Alm_unrLo  ']
df_new['Nominal_HiLim1'] = df_copy['Alm_preHi  '] 
df_new['Nominal_LoLim1'] = df_copy['Alm_preLo  ']
""" 


# In[151]:


df_new.head(15)


# In[152]:


#df_analog['EU_Hi  '] = df_analog['EU_Hi  '].apply(keep_decimal_precision)
df_new['pScale EU_Hi'] = df_analog['EU_Hi  ']


# In[153]:


df_new


# # STN 

# In[154]:


df_analog['Key'] = df_analog['Name  '].str.split(',').str[0].str.strip()

stn_values = []

for i in range(len(df_analog)):
    
    matching_row = df_station[df_station['Key'] == df_analog.loc[i, 'Key']]
    
    if not matching_row.empty:
        stn_values.append(f"{matching_row['Order'].values[0]:03}")
    else:
        stn_values.append(np.nan)
df_new['Stn'] = stn_values


# In[155]:


df_new


# # KEY

# In[156]:


cols = ['Alm_unrHi', 'Alm_unrLo', 'Alm_preHi', 'Alm_preLo', '78,1', '78,4', '77,1', '77,4']
for col in cols:
    if col not in df_new.columns:
        df_new[col] = np.nan



# In[157]:


key_values = []
xx_yyy_counters = {}


# In[158]:


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


# In[159]:


df_new


# In[160]:


#df_new = df_new[['record', 'OrderNo','Type', 'Key', 'Name', 'Stn', 'AOR', 'Nominal_HiLim', 'Nominal_HiLim1', 'Nominal_LoLim', 'Nominal_LoLim1', 'pScale EU_Hi', 'AlarmGrp']].copy()
#df_new['ICAddress'] = "NaN"


# In[161]:


df_new


# df_ner['NominalPairInactive'] 

# In[162]:


new_column_order = ['record', 'OrderNo', 'Type', 'Key', 'Name', 'Stn', 'AOR',
                    '77,0', '77,1', '77,2', '77,3', '77,4',
                    '78,0', '78,1', '78,2', '78,3', '78,4',
                    '91,1', '91,2', '91,3', '91,4', '91,5',
                    'pScale EU_Hi', 'AlarmGrp', 'ICAddress']


df_new = df_new[new_column_order]



# In[163]:


df_new


# In[164]:


df_new['Key'] = '"'+ df_new['Key'].str.rstrip() + '"'
df_new['Name'] = '"'+ df_new['Name'].str.rstrip() + '"'


# In[166]:


df_new


# Output Filename:

# In[167]:


output_analog_name = 'Analog99.dat'


# In[168]:


with open(output_analog_name, 'w') as f:
    f.write('* \n')
    f.write('\t5\tANALOG\t0\t0\t1\t3\t4\t5\t10\t24\t42\t77,0\t77,1\t77,2\t77,3\t77,4\t78,0\t78,1\t78,2\t78,3\t78,4\t91,1\t91,2\t91,3\t91,4\t91,5\t66\n')
    f.write('*record  OrderNo  Type  Key  Name  Stn  AOR  pScale EU_Hi AlarmGrp   Nom.HiLim:77,0  77,1  77,2  77,3  Rsnblty77,4  Nom.LoLim78,0  78,1  78,2  78,3  Rsnblty78,4  NomPairInactive91,1  91,2  91,3  91,4  91,5  ICAddress\n')

    for index, row in df_new.iterrows():
        f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format
                ("", row['record'], row['OrderNo'], row['Type'], row['Key'], row['Name'], row['Stn'], row['AOR'],row['pScale EU_Hi'], row['AlarmGrp'], row['77,0'], row['77,1'], row['77,2'], row['77,3'], row['77,4'], row['78,0'], row['78,1'], row['78,2'], row['78,3'], row['78,4'], row['91,1'], row['91,2'], row['91,3'], row['91,4'], row['91,5'], row['ICAddress']))
    f.write(" 0")  


# In[169]:


comment= """ indent_format = "{:<10}" 
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
    f.write('* \n')

    
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
               
                icaddress_format.format(df_new.loc[i, 'ICAddress']) + '\n') """


# # ANALOG_CONFIG

# vamos a crear un dataframe llamado Analog_config , el cual tendrá solo dos columnas, una columna se llamara Key , cuyo contenido será exactamente el contenido de Key del df  llamado df_new . y una columna se llamara name , que vendra de df_analog['Name  '] 

# In[170]:


Analog_config = pd.DataFrame({
    'Key': df_new['Key'],
    'name': df_analog['Name  '].str[3:].str.strip()  # Obtener los caracteres a partir del tercer carácter en cada fila
})

# Crear una función para buscar el número en df_device_instance
def find_number(name):
    match = df_device_instance[df_device_instance['Name  '] == name]
    if not match.empty:
        return match.iloc[0]['Number']
    else:
        return None

# Aplicar la función para obtener los números y almacenarlos en Analog_config['pDeviceInstance']
Analog_config['pDeviceInstance'] = Analog_config['name'].apply(find_number)

# Ahora, Analog_config contendrá la columna 'pDeviceInstance' con los números correspondientes.


# In[307]:





# In[171]:


Analog_config


# In[172]:


Analog_config.drop('name', axis=1, inplace = True )


# In[173]:


Analog_config


# In[174]:


Analog_config.to_csv('AnalogConfig.csv', index=False)


# In[176]:


with open('ANALOG_CONFIG.dat', 'w') as f:
    f.write("*\n")
    f.write("*\n")
    f.write("\t41\tANALOG_CONFIG\t0\t9\n")
    f.write("*--KEY---pDeviceInstance----------------------------------\n")

    for index, row in Analog_config.iterrows():
        f.write("\t{}\t{}\n".format(row['Key'], row['pDeviceInstance']))
    
    f.write(" 0")


# In[ ]:




