#!/usr/bin/env python
# coding: utf-8

# # 1.County

# Supports U.S county names, valid for both upper case and lower case. 
# Accounts for both cases, with and without suffix "county". Eg: Allows both "Tippecanoe" and "Tippecanoe County" 

# In[94]:


import geonamescache                      #County library
gc = geonamescache.GeonamesCache()
co = gc.get_us_counties()
counties = []

for i in co:                             #Creating a list of all counties
    counties.append(i['name'].upper())   #Keeping them all in upper case
    if i['name'].find(' County') != -1:  #Creating cases with and without county suffix
        counties.append(i['name'].replace(' County','').upper())

def county_chk(strn):                    #Checks if passed string is a county
    '''Function to detect the validity of the county name'''
    if strn.upper() not in counties:
        return 'Not Valid'
    else:
        return 'Valid'


# 
# # 2.Cities

# Supports major cities all across the world. Valid for both upper case and lower case.
# 

# In[147]:


import geonamescache
gc = geonamescache.GeonamesCache()
c = gc.get_cities()
cities = [c[key]['name'] for key in list(c.keys())]         #Creating a list of cities
cities = list(map(lambda x:x.upper(), cities))              #Converting them all to upper case
cities = [x for x in cities if str(x) != 'NAN']             #Removing NULL value
cities.remove('MALE')                                       #Remove city name male, since it causes confusion with gender entity

def city_chk(strn):                                         #Checks if passed string is in the cities list
    '''Function to detect the validity of the city name'''
    if strn.upper() in cities:
        return 'Valid'
    else:
        return 'Not Valid'


# # 3.States

# Supports U.S state names, valid for both upper case and lower case. Allows both full state name and alpha codes. Eg: "Indiana" and "IN"

# In[96]:


import geonamescache
gc = geonamescache.GeonamesCache()
st = gc.get_us_states()
stcode = []
states = []
for i in st:
    stcode.append(st[i]['code'])                             #List of alpha codes of states
    states.append(st[i]['name'].upper())                     #List of state names

def state_chk(strn):
    '''Function to detect the validity of the state name'''
    chk = 0
    if strn.upper() in states or strn.upper() in stcode:
        return 'Valid'
    else:
        return 'Not Valid'


# 
# # 4.Countries

# Supports country names across the globe, valid for both upper case and lower case. Allows colloquial name, official name, official two character and three character alpha codes. Eg: "United States", "United States of America", "US", "USA"

# In[156]:


import pycountry
cntrs = list(pycountry.countries)
c_name = []
official_name = []
alpha_2 = []
alpha_3 = []
for i in cntrs:
    c_name.append(i.name.upper())                      #Common name list
    if i.name.find(',')!=-1:
        c_name.append((i.name[i.name.find(',')+2:]+' '+i.name[:i.name.find(',')]).upper())
    for j in ('IRAN','RUSSIA','SOUTH KOREA','KOREA','VIETNAM','BOLIVIA','TAIWAN','UK','SYRIA','VENEZUELA'): #Adding a few commonly used name structures which are stored differently in the library 
        c_name.append(j)
    try:
        official_name.append(i.official_name.upper())  #Official name list
    except:
        pass
    alpha_2.append(i.alpha_2)                          #Two character alpha list
    alpha_3.append(i.alpha_3)                          #Three character alpha list
    

def country_chk(strn):
    '''Function to detect the validity of the country name'''
    chk = 0
    if strn.upper() in c_name or strn.upper() in official_name or strn.upper() in alpha_2 or strn.upper() in alpha_3:
        return 'Valid'
    else:
        return 'Not Valid'


# # 5.Currency

# Detects popular currencies upto 2 decimal points. Supported currency representations: $, USD, usd, CAD, €, EUR, EURO, euro, eur, £, JPY, ¥, CNY, GBP

# In[98]:


def currency_chk(amount):
    '''Function to detect popular currencies'''
    import re
    regex = re.compile(r'^(\$|USD|usd|CAD|€|EUR|EURO|euro|eur|£|JPY|¥|CNY|GBP)\s?(\d*(\d\.?|\.\d{1,2}))$') #All the currency representations we are testing for
    result = regex.match(amount)    #Matching the entered string with our stored characters
    if result:
        return('Valid')
    else:
        return('Not Valid')
    


# # 6.Phone Number

# Detects following formats
# 1. 000-000-0000
# 2. 000 000 0000
# 3. 000.000.0000
# 4. (000)0000000
# 5. 0000000000
# 
# Maximum of 12 digits and minimum of 6 digits is allowed
# 

# In[99]:


def phone_chk(number):
    '''Function to detect phone numbers'''
    if len(number)<=12 and len(number)>=6:
        import re
        regex=re.compile(r'^\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}')  #All the formats that are being checked
        result = regex.match(number)             #Matching the entered string with our stored characters
        if result:
            return 'Valid'
        else:
            return 'Not Valid'
    else:
        return 'Not Valid'


# # 7.Credit Card

# Uses Luhn Algorithm to detct the credit card detections
# 
#  https://en.wikipedia.org/wiki/Payment_card_number
#  
#  https://en.wikipedia.org/wiki/Luhn_algorithm
#  
#  https://www.geeksforgeeks.org/luhn-algorithm/
#  
#  Number of digits allowed : 13-19
#         
# Working Credit Cards under this Algo: 
# 1. AMEX
# 2. Bankcard
# 3. Diners Club enRoue
# 4. Discover Card
# 5. RuPay
# 6. InterPayment
# 7. JCB
# 8. Laser
# 9. Maestro
# 10. Dankort
# 11. MIR
# 12. NPS Pridnestrovie
# 13. Mastercard
# 14. Solo
# 15. Switch
# 16. Troy
# 17. Visa
# 18. UATP
# 19. Verve

# In[100]:


def credit_card_chk(card_number):
    '''Function to detect whether credit card is valid or not by its card number. Dev. by using Luhn algo'''
    if len(card_number)>=13 and len(card_number)<=19:   # filtering the length of credit cards between 13 and 19
        try:
            cc_list=[int(d) for d in str(card_number)]  #creating the list of string credit cards
            odd_digits = cc_list[-1::-2]                #creating the list of odd digits of the credit card
            even_digits = cc_list[-2::-2]               #creating the list of even digits of the credit card
            cc_digits_sum = 0                           #initiating the cc_digits_sum as zero
            cc_digits_sum += sum(odd_digits)            #adding all the odd digits of the credit card
            for d in even_digits:                       #logic for even digits of the credit card
                d*=2                                        
                if d > 9:
                    d= d-9 
                cc_digits_sum=cc_digits_sum + d
            if cc_digits_sum % 10==0:                   #if remainder of cc_digits_sum divided by 10 is zero; cc is valid 
                return 'Valid'
            else:
                return 'Not Valid'
        except:
            return 'Not Valid'
    else:
        return 'Not Valid'
        


# # 8.Mail ID

# Mail ID starting character should be aplhamnumeric. 
# Should have 2 or 3 characters at the end after '.'

# In[101]:


def email_chk(val):    
    '''Function to detect the validity email'''
    import re
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'  ##All the email formats that are being checked
    c=0
    if(re.search(regex,val)):                      #Matching the entered string with our stored characters
         return 'Valid'
    else:
        return 'Not Valid'


# # 9.URL

# URL should start with http:// or https://, can have any alphanumeric domain name and must end with two or more characters after the '.'
# It also incorporates URLs with IP or server addresses like "http://localhost:8889/notebooks/Functions_Data%20Profiling.ipynb"
# 

# In[102]:


def url_chk(val):    
    '''Function to detect the validity email'''
    import re
    a=0
    regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if (re.match(regex, val) is not None) == True:
        return 'Valid'
    else:
        return 'Not Valid'


# # 10.Month

# Detects months where the input is either the entire name or the three character short form. Not checking for numbers, since this would cause other numeric fields to be identified as months when their range is under 12

# In[103]:


month=['jan','january','feb','february','mar','march','apr','april','may','jun','june','jul','july','aug','august','sep','september','oct','october','nov','november','dec','december']
def month_chk(string):
    import re
    string=string.lower()                       #converting the string to lower case
    if string in month:                         #Matching the entered string with the month list created
        return 'Valid'
    else:
        return 'Not Valid'
    


# 
# # 11.Temperature

# Works with
# 1. Positive and negative sign for the temperature
# 2. After decimal 2 digits only
# 3. Temperature symbol can be [CcFf]
# 4. Space or no-space between ineteger and the temp (CcFf) symbol
# 

# In[104]:


def temperature_chk(string):
    import re
    regex=re.compile(r"([+-]?((\d*(\d\.?|\.\d{1,2}))\s?°?(?i)(\W|^)(C|c|F|F)(\W|$)))")
    result=regex.match(string)              #Matching the entered string with our stored characters
    if result: 
        return 'Valid'
    else:
        return 'Not Valid'


# # 12.Distance

# In[105]:


def distance_chk(string):
    import re
    regex=re.compile(r"((\d*(\d\.?|\.\d{1,2}))\s?(?i)(\W|^)(KMS|km|miles|mile|INCH|M|feet|ft)(\W|$))")
    result=regex.match(string)          #Matching the entered string with our stored characters
    if result:
        return 'Valid'
    else:
        return 'Not Valid'


# # 13.Date

# Checks for dates of the following formats:
# 1. yyyy-m-d
# 2. yyyy-d-m
# 3. yy-m-d
# 4. yy-d-m
# 5. m-d-yyyy
# 6. m-d-yy
# 7. d-m-yyyy
# 8. d-m-yy
# 
# Also checks for same formats even when / is used instead of -
# 
# Added the functionality to check if a numeric value could possibly be a date. For eg 02032020, 02 03 2020. Have checked for all the above date formats in this numeric manner as well

# In[125]:


import datetime
def date_chk(date_time_str):
    try:                                                             #Logic to check if an entered number could possibly be a date
        num = date_time_str.replace(' ','')
        if len(num) == 6:
            if (100>int(num[:2])>=90) or (int(num[:2])<25):
                if int(num[2:4])<=12 and int(num[4:])<=31:
                    return 'Valid'
                if int(num[2:4])<=31 and int(num[4:])<=12:
                    return 'Valid'
            if (100>int(num[:2])>=90) or (int(num[:2])<25):
                if int(num[:2])<=12 and int(num[2:4])<=31:
                    return 'Valid'
                if int(num[:2])<=31 and int(num[2:4])<=12:
                    return 'Valid'
        if len(num) == 8:
            if int(num[:4])>=1990 and int(num[:4])<2025:
                if int(num[4:6])<=12 and int(num[6:])<=31:
                    return 'Valid'
                if int(num[4:6])<=31 and int(num[6:])<=12:
                    return 'Valid'
            if int(num[-4:])>=1990 and int(num[-4:])<2025:
                if int(num[:2])<=12 and int(num[2:4])<=31:
                    return 'Valid'
                if int(num[:2])<=31 and int(num[2:4])<=12:
                    return 'Valid'
    except:
        pass
    
    if date_time_str.find('/') == -1 and date_time_str.find('-') == -1:    #Logic to check if a string entry is a date
        return 'Not Valid'
    try:
        datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
        return 'Valid'
    except:
        pass

    try:
        datetime.datetime.strptime(date_time_str, '%y-%m-%d')
        return 'Valid'
    except:
        pass

    try:
        datetime.datetime.strptime(date_time_str, '%Y-%d-%m')
        return 'Valid'
    except:
        pass

    try:
        datetime.datetime.strptime(date_time_str, '%y-%d-%m')
        return 'Valid'
    except:
        pass

    try:
        datetime.datetime.strptime(date_time_str, '%Y/%m/%d')
        return 'Valid'
    except:
        pass

    try:
        datetime.datetime.strptime(date_time_str, '%y/%m/%d')
        return 'Valid'
    except:
        pass

    try:
        datetime.datetime.strptime(date_time_str, '%Y/%d/%m')
        return 'Valid'
    except:
        pass

    try:
        datetime.datetime.strptime(date_time_str, '%y/%d/%m')
        return 'Valid'
    except:
        pass

    try:
        datetime.datetime.strptime(date_time_str, '%m-%d-%Y')
        return 'Valid'
    except:
        pass

    try:
        datetime.datetime.strptime(date_time_str, '%m-%d-%y')
        return 'Valid'
    except:
        pass

    try:
        datetime.datetime.strptime(date_time_str, '%d-%m-%Y')
        return 'Valid'
    except:
        pass

    try:
        datetime.datetime.strptime(date_time_str, '%d-%m-%y')
        return 'Valid'
    except:
        pass

    try:
        datetime.datetime.strptime(date_time_str, '%m/%d/%Y')
        return 'Valid'
    except:
        pass

    try:
        datetime.datetime.strptime(date_time_str, '%m/%d/%y')
        return 'Valid'
    except:
        pass

    try:
        datetime.datetime.strptime(date_time_str, '%d/%m/%Y')
        return 'Valid'
    except:
        pass

    try:
        datetime.datetime.strptime(date_time_str, '%d/%m/%y')
        return 'Valid'
    except:
        pass

    return 'Not Valid'

   


# # 14.Time

# Checks for the following formats of time:
# 1. HH:MM
# 2. HH:MM:SS

# In[107]:


def time_chk(date_time_str):
    if date_time_str.find(':')==-1:
        return 'Not Valid'
    try:
        datetime.datetime.strptime(date_time_str, '%H:%M')
        return 'Valid'
    except:
        pass
    try:
        datetime.datetime.strptime(date_time_str, '%H:%M:%S')
        return 'Valid'
    except:
        pass
    try:
        datetime.datetime.strptime(date_time_str, '%H:%M:%S.%f')
        return 'Valid'
    except:
        pass
    
    return 'Not Valid'


# # 15. Animals

# Checking for anmials from an online repository, case insensitive

# In[108]:


import urllib.request
target_url = "https://gist.githubusercontent.com/atduskgreg/3cf8ef48cb0d29cf151bedad81553a54/raw/82f142562cf50b0f6fb8010f890b2f934093553e/animals.txt"
animals = list()
for line in urllib.request.urlopen(target_url):               #list of animals
        animals.append(line.decode('utf-8')[:-1].lower())    
def animal_chk(string):
    if string.lower() in animals:                          #Matching the entered string with animals list
        return 'Valid'
    else:
        return 'Not Valid'


# # 16. Name

# Using a spacy model "en_core_web_sm" to check if a string could possibly be a name

# In[109]:


#Can be installed from the below link
#pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.0/en_core_web_sm-2.2.0.tar.gz
import en_core_web_sm                               #importing en_core_web_sm using spacy model "en_core_web_sm"
nlp = en_core_web_sm.load()                          


# In[110]:


def name_chk(string):
    test = nlp(string.lower())                       
    for X in test:                                   #Matching the entered string 
        if X.ent_type_=='PERSON':
            return 'Valid'
    return 'Not Valid'


# # 17. Gender

# Check if input string is a gender. Considering either male and female or m and f

# In[134]:


def gender_chk(string):
    if string.lower() in ['male','female']:         #Matching the entered string with the list 
        return 'Valid'
    if string.lower() in ['m','f']:                 
        return 'Valid'
    return 'Not Valid'


# # 18. Binary

# Checking if input is binary data, 1 and 0, or true and false, or t and f. Later validating that the column does in fact hold binary data by validating against unique values

# In[112]:


def binary_chk(string):
    try:
        if int(string) in [1,0]:                    #Matching the entered string with the list
            return 'Valid'
    except:
        pass
    if string.lower() in ['true','false']:
        return 'Valid'
    if string.lower() in ['t','f']:
        return 'Valid'
    return 'Not Valid'


# # 19. Datetime

# Checking for datetime data by splitting input data and running it against both date and time functions. Supported formats:
# 1. Date Time
# 2. Time Date

# In[113]:


def datetime_chk(string):
    try:
        dtm = string.split()                                                #splitting into string
        if len(dtm) == 2:                                                   #Checking if individual parts are date and time
            if date_chk(dtm[0]) == 'Valid' and time_chk(dtm[1]) == 'Valid':  
                return 'Valid'
            if date_chk(dtm[1]) == 'Valid' and time_chk(dtm[0]) == 'Valid':
                return 'Valid'
    except:
        pass
    return 'Not Valid'        


# # 20. SSN

# Checking if SSN is entered in the following format: ddd-dd-dddd

# In[160]:


def ssn_chk(ssn):
    try:
        chunks = ssn.split('-')
        if len(chunks) ==3: 
            if len(chunks[0])==3 and len(chunks[1])==2 and len(chunks[2])==4:
                tst = int(chunks[0]+chunks[1]+chunks[2])
                return 'Valid'
        return 'Not Valid'
    except:
        return 'Not Valid'


# In[114]:


#Setting such that warnings, in case of any, aren't displayed in between the output

import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")


# # Graphs

# In[115]:


def graph(data,filename):
    data_1=pd.read_csv(data)                                    #reading the data file
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    col_num=[]                                                  #intiating the blank lists
    col_str=[]                                                          
    for col in data_1:
        try:
            pd.to_numeric(data_1[col])                          #coverting the string to numeric
            col_num.append(col)                                 #appending to col_num list if it got converted to numeric
        except:
            col_str.append(col)                                 #appending to col_str list if it not converted to numeric
    col= col_num + col_str                                      
    y=len(col)
    x=(y//2)+1  
   
    with PdfPages('EDA_Synopysis.pdf') as pdf:                  #creating the graphs pdf file
        plt.figure(figsize=(4*x,6*x))
        plt.grid(False)
        plt.suptitle('Exploratory Data Analysis',fontsize=50,fontweight='bold')
        
        for i in range(1,y+1):
            plt.subplot(x,2,i,facecolor=(1,1,1))
            if col[i-1] in col_num:
                plt.hist(data_1[col[i-1]],bins=10,color="lightseagreen")     #histogram for numeric data type
                plt.title(col[i-1]+' Histogram', fontsize=35)
               
            else:
                freq =data_1[col[i-1]].value_counts()
                l1=[]
                l2=[]
                for j in range(3):
                    t3f=[]
                    try:
                        val = freq[j]
                    except:
                        break
                    if val == 1:
                        if j == 0:
                            print('N/A')
                        break
                    l1.append(freq.keys()[j])
                    l2.append(val)
                plt.barh(l1, l2, align='center', alpha=1,color="lightseagreen") #bar chart for string data type
                plt.title(col[i-1]+'- Top frequency counts', fontsize=35)
                
        pdf.savefig()  # saves the current figure into a pdf page
        plt.close()


# Sampling the data:

# In[116]:


def sample(data):
    '''Random sampling of data'''
    if data.shape[0] > 999:                                     #checking if number of rows is greater than 999
        if data.shape[0] > 3333:                                #if rows is greater than 3333, taking 1000 rows as sample
            return data.sample(n = 1000, random_state=1)
        return data.sample(frac=0.3, random_state=1)            # if rows between 999 and 3333, taking 30% of the data
    else: 
        return data                                             #if the rows below 999 taking full sample


# List of entity columns to be tested

# In[165]:


funclist = [county_chk,city_chk,state_chk,country_chk,currency_chk,phone_chk,credit_card_chk,email_chk,url_chk,date_chk,time_chk,distance_chk,temperature_chk,month_chk,animal_chk,name_chk,gender_chk,binary_chk,datetime_chk,ssn_chk]
funclist_num = [phone_chk,credit_card_chk,binary_chk,date_chk]


# Confidence Score Function:

# In[166]:


import random
from prettytable import PrettyTable
def cscore(data):
    '''Function to calculate the confidence score for each column'''
    print('\nCONFIDENCE SCORES:\n ')
    data = sample(data)
    data_dict = data.to_dict()                                 #converting dataframe to dictionary for performance
    x = PrettyTable()                                          #Pretty table to improve output presentation
    x.field_names = ["Column Name", "Tested Entity", "Confidence Score"]
    
    for i in data_dict.keys():                                 #Iterating through all the columns
        u = data[i].nunique()                                  #Unique count in column
        cnt = data[i].count()                                  #Count of non null values
        try:                                                   #If numeric column, checking for fewer entities. To improve runtime
            pd.to_numeric(data[i])
            func = funclist_num
        except:
            func = funclist
        chk = 0
        for j in func:                                         #Iterating through every entity function
            func_str = str(j)[10:str(j).find('at ')-5]         #Getting the name of entity from the function name
            if (func_str == 'name' or func_str == 'city' or func_str == 'county') and len(data_dict[i].items())>300:     #Limiting testing values for name entity check to improve runtime
                d2 = dict((k,j(str(v))) for k, v in random.sample(data_dict[i].items(),k=300))
            else:    
                d2 = dict((k,j(str(v))) for k, v in data_dict[i].items())
            d3= {k:(1 if v=='Valid' else 0 ) for (k,v) in d2.items()}
            a=[v for v in d3.values()]
            accuracy=round((sum(a)/cnt)*100,2)               #calculating the confidence score(proper fit score)
            if func_str == 'binary' and u!=2:
                accuracy = 0
            if accuracy != 0:
                l=[]
                if chk == 0:
                    l.append(str(i))
                else:
                    l.append(' ')
                l.append(func_str)
                l.append(str(accuracy))
                x.add_row(l)
                chk = 1
    print(x)


# Performing basic EDA

# In[167]:


import matplotlib.pyplot as plt
def eda(data):
    rw = data.shape[0]
    print('Rows: ',str(rw))
    print('Columns: ',str(data.shape[1]),'\n')
    pk = []                                                       #List to store columns that are possible primary keys
    mis = []                                                      #List to store columns with missing data
    from prettytable import PrettyTable

    for col in data:                                             
        print('Column Name:',col)                                 
        u = data[col].nunique()
        print('Unique Value Count:',u)
        if u == rw:
            pk.append(col)
        n = data[col].size - data[col].count()
        print('Null Count:',n)
        if n != 0:
            mis.append(col)
        try:                              
            pd.to_numeric(data[col])                                #calculating mean, median for numeric data types
            print('Mean', round(data[col].mean(),2))
            print('Median',round(data[col].median(),2))
            
            plt.style.use('ggplot')
            plt.hist(data[col], bins=10,color="lightseagreen")      # plotting histogram for numeric data types
            plt.show()
            print('\n')
            continue
        except:
            freq = data[col].value_counts()
            print('Top Three Frequency Values:')
            y = PrettyTable()
            y.field_names = ["Value", "Count"]
            l1=[]
            l2=[]
            for i in range(3):                                       #Making the list of top three by count freq
                t3f=[]
                #l1=[]
                #l2=[]
                try:
                    val = freq[i]
                except:
                    break
                if val == 1:
                    if i == 0:
                        print('N/A')
                    break

                t3f.append(freq.keys()[i])                        
                l1.append(freq.keys()[i])
                t3f.append(val)
                l2.append(val)
                y.add_row(t3f)
            print(y)
            plt.barh(l1, l2, align='center', alpha=1,color="lightseagreen") #plotting the bar graph for top three coutn freq 
            plt.show()
            
            
        print('\n')
    print ('Possible Primary Key(s):',pk)
    print ('Columns with missing data:',mis,'\n')
    print('\n')
        


# In[168]:


import os  
import pandas as pd

def db(filename):
    df = pd.read_csv(filename, index_col=None, header=0)          #reading the input csv file
    print('\n')
    print('----------------------',os.path.basename(filename),'----------------------')
    print('DATA SUMMARY:\n')
    eda(df)
    cscore(df)
    
def graphs(filename):
    df = pd.read_csv(filename, index_col=None, header=0) 
    graph(df,filename)
    

