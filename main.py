#!/usr/bin/env python
# coding: utf-8

# FEP , CHANNEL , and RTU_DATA
# ---------------

# ------------

# # FEP

# FEP dependencies: 
# 
# Indic 0             mapping:  1               (create only one record)
# 
# Mode   2            mapping:  1               (create only one record)
# 
# Hostname  4         mapping:  fepts01         (create only one record)
# 
# Name   5            mapping:  Comm_Server_1   (create only one record)
# 
# NumPorts 11         mapping:  16              (create only one record)
#  
# ipdaddress  17      mapping:  192.168.32.16   (create only one record)

# In[2]:


import pandas as pd
from datetime import datetime
#libraries


# In[17]:


data = {
    'Indic': [1],
    'Mode': [1],
    'Hostname': ['fepts01'],
    'Name': ['Comm_Server_1'],
    'NumPorts': [11],
    'ipdaddress': ['192.168.32.16']
}

FEP = pd.DataFrame(data)

print('Preview \n',FEP)


# In[15]:


date_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open('FEP.DAT', 'w') as file:
    file.write('*' * 88 + '\n')
    file.write('*  Creation Date/Time:  ' + date_string + '\n')
    file.write('*' * 88 + '\n')
    file.write('*             Indic  Mode  Hostname             Name      NumPorts         ipaddress\n')
    file.write('*             -----  ----  --------             ----      --------         ---------\n')
    file.write('   4 FEP          0     2         4                5            11                17\n')
    for index, row in FEP.iterrows():
        file.write(f'                  {row["Indic"]}     {row["Mode"]}   {row["Hostname"]}    {row["Name"]}            {row["NumPorts"]}     {row["ipdaddress"]}\n')


# # CHANNEL

# dependencies: 
# 
# 
# pFEP 1          mapping: Set all to 1   [Build: If not mapped will be manually configured by PE]
# 
# Character 13    mapping: Set all to 8
# 
# Stop_Bits 14    mapping: Set all to 1
# 
# Name  19       [COMM.csv] mapping: Desc 
# 
# baudrate 23    [COMM.csv] mapping: Comm_Line   . Detailed mapping : 9600
# 
# ChannelRespTimeoutMsec 24  [COMM.csv] mapping: Pri_Resp_TO
# 
# PhysicalPort 25    [COMM.csv]  mapping: Comm_Line
# 
# Hostname  30    mapping:  Set all to 1
# 
# ChannelConnTimeout 41   [COMM.csv]  mapping:  Pri_Resp_TO
# 
# 

# _Comm.csv_ Should be in the same folder

# In[4]:


comm_data = pd.read_csv('Comm.csv')

channel = pd.DataFrame()

#COLUMNS OF CHANNEL 

channel['pFEP'] = [1] * len(comm_data)
channel['Character'] = [8] * len(comm_data)
channel['Stop_Bits'] = [1] * len(comm_data)
channel['Name'] = comm_data['Desc  ']
channel['baudrate'] = [9600] * len(comm_data)
channel['ChannelResTimeoutMsec'] = comm_data['Pri_Resp_TO  ']
channel['PhysicalPort'] = comm_data['Comm_Line  ']
channel['Hostname'] = [1] * len(comm_data)
channel['ChannelConnTimeout'] = comm_data['Pri_Resp_TO  ']


# In[5]:


channel


# Controlar : 
# 
# channel['ChannelResTimeoutMsec'] = comm_data['Pri_Resp_TO  ']
# 
# channel['ChannelConnTimeout'] = comm_data['Pri_Resp_TO  '] 
# 
#   (Mismo output en ambas columnas)
#   
# 
# _baudrate_ : el documento mapping hace referencia a la columna Comm_Line (Exactamente igual que PhysicalPort), Pero en detailed mapping figura solamente el entero "9600" . se procedió a rellenar toda la columna con ese número hasta próxima instrucción .
# 
# 

# # Output : Channel.DAT

# In[45]:


#Width definition. 
indent_format = "{:<10}"  # Initial TAB
indent2 = "{:1}"
type_format = "{:<7}"
key_format = "{:<9}"
name_format = "{:<13}"
stn_format = "{:<32}"
aor_format = "{:<12}"
pstate_format = "{:<25}"
norm_format = "{:<15}"
alarmgroup_format = "{:<13}"
icaddress_format = "{:<20}"


with open('Channel.dat', 'w') as f:
    f.write('*         pFEP   Character   Stop_Bits       Name                            baudrate     ChannelResTimeoutMsec    PhysicalPort   Hostname     ChannelConnTimeout\n')
    f.write('*         ----   ---------   ---------       -------------------------       --------     ---------------------    ------------   --------     ------------------\n')
    f.write(' CHANNEL     1          13          14                              19             23                        24              25         30                     41\n')

    for i in range(len(channel)):
        f.write(indent_format.format('') + 
                type_format.format(channel.loc[i, 'pFEP']) +
                key_format.format(channel.loc[i, 'Character']) + 
                indent2.format('') + 
                indent2.format('') + 
                indent2.format('') + 
                name_format.format(channel.loc[i, 'Stop_Bits']) +
                indent2.format('')+
                indent2.format('') + 
                indent2.format('') + 
                stn_format.format(channel.loc[i, 'Name']) +
                aor_format.format(channel.loc[i, 'baudrate']) + 
                indent2.format('')+
                pstate_format.format(channel.loc[i, 'ChannelResTimeoutMsec']) +
                norm_format.format(channel.loc[i, 'PhysicalPort']) +
                alarmgroup_format.format(channel.loc[i, 'Hostname']) +
                icaddress_format.format(channel.loc[i, 'ChannelConnTimeout']) + '\n')


# # RTU_DATA

# dependencies:
# 
# 
# Indics           0  [RTU.csv] column: RTU_Number      . SEE KEY Strategy
#   
# pCHANNEL_GROUP   2  [RTU.csv] column: Comm_Line        If not mapped will be manually configured by PE
# 
# Protocol         3  [RTU.csv] column: Scan_Task   Mapping: Set all to 8.  If not mapped will be set to 1 (NONE)
# 
# Name             5  [RTU.csv] column: Desc       Mapping: Desc='BRAZ ICCP VRTU' can be deleted . If not mapped will be < Station >_<##>
# 
# Address          14 [RTU.csv] column: RTU_Number   Mapping: if == 8, "", else RTU_Number 
# 
# 

# RTU.csv should be in the same folder

# OBSERVACIONES: 
# Protocol 3 : referido hacia columna Scan_Task (en objeto RTU DATA ), no existe en RTU.csv , Igualmente acorde al mapping debe ser seteado todo a 8
# 
# 
# Indics.  Referencia particularmente a la columna RTU_ Number.  Pero tambien indica "See key strategy" , para lo cual indica como realizar una key basandose en una estación , al no tener dicha información solo se considerará el numero declarado por la columna RTU_Number . 

# In[46]:


rtu_data = pd.read_csv('RTU.csv')


# In[47]:


df = pd.DataFrame()

#CHECK INDICS ******************
df['Indics'] = rtu_data['RTU_Number  ']

df['pCHANNEL_GROUP'] = rtu_data['Comm_Line  ']
df['Protocol'] = [8] * len(rtu_data)
df['Name'] = rtu_data['Desc  ']
df['Address'] = rtu_data['RTU_Number  ']
# Condition :   df['Address'] : if == 8 , value = "", else RTU Number
df['Address'] = df['Address'].apply(lambda x: '' if x == 8 else x)


# In[57]:


df


# # OUTPUT : RTU.DAT

# In[64]:


#Width definition. 
indent_format = "{:<10}"  # Initial TAB
indent2 = "{:1}"
type_format = "{:<9}"
key_format = "{:<14}"
name_format = "{:<13}"
stn_format = "{:<32}"
aor_format = "{:<12}"
pstate_format = "{:<25}"

with open('RTU.dat', 'w') as f:
    f.write('*         Indics   pCHANNEL_GROUP   Protocol        Name                            Address\n')
    f.write('*         ------   --------------   --------        -------------------------       --------\n')
    f.write(' RTU           0                2          3                                5             14\n')

    for i in range(len(df)):
        f.write(indent_format.format('') + 
                type_format.format(df.loc[i, 'Indics']) +
                key_format.format(df.loc[i, 'pCHANNEL_GROUP']) + 
                indent2.format('') + 
                indent2.format('') + 
                indent2.format('') + 
                name_format.format(df.loc[i, 'Protocol']) +
                indent2.format('')+
                indent2.format('') + 
                indent2.format('') + 
                stn_format.format(df.loc[i, 'Name']) +
                aor_format.format(df.loc[i, 'Address']) + '\n')


# In[ ]:




