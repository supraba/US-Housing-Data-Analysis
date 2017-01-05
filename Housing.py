import pandas as pd
import numpy as np
import re
from scipy.stats import ttest_ind

def main():
	run_ttest()
  
def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    stData = []
    ciData = []
    myfile = open('university_towns.txt','r')
    strLine = myfile.read().split("\n")
    city=''
    state=''
    for iStr in strLine:
        if iStr.find("edit") == -1:
            city = re.sub('\[.*', '', iStr)
            city = re.sub('\(.*', '', city).strip()
            if city!="":
                stData.append(state)
                ciData.append(city)
        else:
            state = re.sub('\[.*\]', '', iStr).strip()
    df = pd.DataFrame({'0':stData,'1':ciData})
    df.columns=['State','RegionName']
    pd.set_option("display.max_rows",520)
    return df
   
  def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    house = pd.read_csv("City_Zhvi_AllHomes.csv")
    exl = pd.ExcelFile("gdplev.xls")
    GDP = exl.parse(header = None, skiprows = 8)
    
    GDP.rename(columns={0:"Current-Dollar and 'Real' Gross Domestic Product: Annual",1:"GDP in billions of current dollars1",2:"GDP in billions of chained 2009 dollars1",4:"Quarterly(Seasonally adjusted annual rates)",5:"GDP in billions of current dollars",6:"GDP in billions of chained 2009 dollars"}, inplace=True)
    GDP.drop({3,7}, axis=1, inplace=True)
    GDP['diffGDP']  = (GDP['GDP in billions of chained 2009 dollars'] - GDP['GDP in billions of chained 2009 dollars'].shift())
    GDP = (GDP.loc[GDP[(GDP['Quarterly(Seasonally adjusted annual rates)'] == '2000q1')].index[0]:, :])
    GDP.drop({"Current-Dollar and 'Real' Gross Domestic Product: Annual","GDP in billions of current dollars1","GDP in billions of chained 2009 dollars1"}, axis=1, inplace=True)
    prev = 0
    curr = 0
    ans = ''
    for row in GDP.index:
        curr = GDP.ix[row]['diffGDP']
        if curr <=0 and prev <= 0:
            ans = GDP.loc[GDP['diffGDP'] == prev,'Quarterly(Seasonally adjusted annual rates)'].values[0]
            break
        prev = curr
    return ans
    
def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    house = pd.read_csv("City_Zhvi_AllHomes.csv")
    exl = pd.ExcelFile("gdplev.xls")
    GDP = exl.parse(header = None, skiprows = 8)
    
    GDP.rename(columns={0:"Current-Dollar and 'Real' Gross Domestic Product: Annual",1:"GDP in billions of current dollars1",2:"GDP in billions of chained 2009 dollars1",4:"Quarterly(Seasonally adjusted annual rates)",5:"GDP in billions of current dollars",6:"GDP in billions of chained 2009 dollars"}, inplace=True)
    GDP.drop({3,7}, axis=1, inplace=True)
    GDP['diffGDP']  = (GDP['GDP in billions of chained 2009 dollars'] - GDP['GDP in billions of chained 2009 dollars'].shift())
    GDP = (GDP.loc[GDP[(GDP['Quarterly(Seasonally adjusted annual rates)'] == '2000q1')].index[0]:, :])
    GDP.drop({"Current-Dollar and 'Real' Gross Domestic Product: Annual","GDP in billions of current dollars1","GDP in billions of chained 2009 dollars1"}, axis=1, inplace=True)
    prev = 0
    curr = 0
    ans = ''
    rec_start = get_recession_start()
    for row,index in GDP.loc[GDP[GDP['Quarterly(Seasonally adjusted annual rates)'] == rec_start].index[0]:,:].iterrows():
        curr = GDP.ix[row]['diffGDP']
        if curr >=0 and prev >= 0 and curr>prev:
            print(curr)
            ans = GDP.loc[GDP['diffGDP'] == curr,'Quarterly(Seasonally adjusted annual rates)'].values[0]
            break
        prev = curr
    return ans
 
 def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    house = pd.read_csv("City_Zhvi_AllHomes.csv")
    exl = pd.ExcelFile("gdplev.xls")
    GDP = exl.parse(header = None, skiprows = 8)
    
    GDP.rename(columns={0:"Current-Dollar and 'Real' Gross Domestic Product: Annual",1:"GDP in billions of current dollars1",2:"GDP in billions of chained 2009 dollars1",4:"Quarterly(Seasonally adjusted annual rates)",5:"GDP in billions of current dollars",6:"GDP in billions of chained 2009 dollars"}, inplace=True)
    GDP.drop({3,7}, axis=1, inplace=True)
    GDP['diffGDP']  = (GDP['GDP in billions of chained 2009 dollars'] - GDP['GDP in billions of chained 2009 dollars'].shift())
    GDP = (GDP.loc[GDP[(GDP['Quarterly(Seasonally adjusted annual rates)'] == '2000q1')].index[0]:, :])
    GDP.drop({"Current-Dollar and 'Real' Gross Domestic Product: Annual","GDP in billions of current dollars1","GDP in billions of chained 2009 dollars1"}, axis=1, inplace=True)
    prev = 0
    curr = 0
    ans = ''
    rec_start = get_recession_start()
    rec_end = get_recession_end()
    for row,index in GDP.loc[GDP[GDP['Quarterly(Seasonally adjusted annual rates)'] == rec_start].index[0]:GDP[GDP['Quarterly(Seasonally adjusted annual rates)'] == rec_end].index[0],:].iterrows():
        curr = GDP.ix[row]['diffGDP']
        if prev <0 and curr>0:
            ans = GDP.loc[GDP['diffGDP'] == prev,'Quarterly(Seasonally adjusted annual rates)'].values[0]
        prev = curr
    return ans

def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    house = pd.read_csv("City_Zhvi_AllHomes.csv")
    list_col = [c for c in house.columns if c.find('19')!=-1]
    house.drop(list_col, axis=1, inplace=True)
    tuples = list(zip(house['State'],house['RegionName']))
    index =  pd.MultiIndex.from_tuples(tuples, names=['State', 'RegionName'])
    # Use this dictionary to map state names to two letter acronyms
    dict = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
    house.replace({"State": dict},inplace=True)
    house.set_index(['State','RegionName'],inplace=True)
    strColList = ['01','02','03','04','05','06','07','08','09','10','11','12']
    for i in range(2000, 2017):
        yrStr = str(i)
        for j in [0,3,6,9]:
            if i == 2016 and j==9:
                break
            if i == 2016 and j == 6:
                ColList = [yrStr+"-"+strColList[j],yrStr+"-"+strColList[j+1]]
            else:
                ColList = [yrStr+"-"+strColList[j],yrStr+"-"+strColList[j+1],yrStr+"-"+strColList[j+2]]
            house[str(i)+"q"+str(int(j/3)+1)] = house[ColList].mean(axis=1)
            house.drop(ColList,axis = 1, inplace=True)
    house.drop(house.columns[[0,1,2,3]],axis = 1, inplace=True)
    return house

def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    hdf = convert_housing_data_to_quarters()
    ul = get_list_of_university_towns()
    ul_list = ul.to_records().tolist() 
    recess_start = get_recession_start()
    recess_bottom = get_recession_bottom()
    before_recess = hdf.columns[hdf.columns.get_loc(recess_start)-1]
    print('%#'+recess_start)
    print('%#'+recess_bottom)
    print('%#'+before_recess)

    hdf['Mean House Price'] = hdf[before_recess].div(hdf[recess_bottom])
    hdf = hdf.loc[:,[before_recess,recess_start,recess_bottom,'Mean House Price']]
    hdf.reset_index(inplace=True)
    hdf=hdf.dropna()
    dfu = pd.merge(ul, hdf, how='inner', on=['State', 'RegionName'])
    dfu.set_index(['State','RegionName'],inplace=True) 
    mask = ~hdf.index.isin(list(map(tuple,dfu)))
    dnfu = hdf.loc[mask]
    p_value = ttest_ind(dfu['Mean House Price'],dnfu['Mean House Price']).pvalue
    different = False
    better = ''
    if p_value<0.01:
        different = True
        better = 'university town'
    print(p_value)
    print(dfu.shape)
    return (different,p_value,better)
