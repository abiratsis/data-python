import pandas as pd
import numpy as np


def avg_gdp(row):
    data = row[['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]
    data.dropna(inplace=True)
    return pd.Series({'avgGDP': np.sum(data) / len(data)})

def germany_gdp_change(row):
    data = row[['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]    
    return np.max(data) - np.min(data)
    
def arrformat(arr):
    return '\n'.join(''.join( '{:15}'.format(e) for e in row) for row in arr)


energy = pd.read_excel(
        io = 'Energy Indicators.xls',
        sheetname = 'Energy',
        header = None,
        skiprows = 18,
        skip_footer = 38,
        index_col = None,
        na_values = ['...'],
        parse_cols = "C:F")

energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']

dic = {'Republic of Korea.*' : 'South Korea',
       'United States of America.*' : 'United States',
       'United Kingdom of Great Britain and Northern Ireland.*' : 'United Kingdom',
       'China, Hong Kong Special Administrative Region.*' : 'Hong Kong',
       '^([A-z]+)\d+$' : r'\1',
       '^([A-z]+)\s\(.*\)$' : r'\1'}

energy['Energy Supply'] = energy['Energy Supply'] * 1000000
energy['Country'].replace(dic, regex = True, inplace = True)
energy.set_index(['Country'], inplace = True)


# len(energy['Country'].unique()) --> 227

#
gdp = pd.read_csv('world_bank.csv', skiprows = 4)

dic = {'Korea, Rep\..*' : 'South Korea', 
       'Iran, Islamic Rep\..*' : 'Iran',
       'Hong Kong SAR, China.*' : 'Hong Kong',
       '^([A-z]+),.*$' : r'\1'
       }

gdp.rename(columns={'Country Name' : 'Country'}, inplace = True)
gdp['Country'].replace(dic, regex = True, inplace = True)
gdp.set_index(['Country'], inplace = True)
gdp = gdp.loc[:, '2006' : '2015']

scim_en = pd.read_excel('scimagojr-3.xlsx', Header = 0)
scim_en.set_index(['Country'], inplace = True)
scim_en = scim_en.sort_values('Rank')

result = scim_en.merge(energy, how='inner', right_index = True, left_index = True).merge(gdp, how = 'inner', right_index = True, left_index = True)

result = result.sort_values('Rank').head(15)

res = result.apply(avg_gdp, axis=1).sort_values('avgGDP', ascending = False)

result['pop'] = result['Energy Supply'] / result['Energy Supply per Capita']
#result.sort_values('pop', ascending = False).iloc[2].name

result['Citable documents per person'] = result['Citable documents'] / result['pop']
pearson_corr = result['Citable documents per person'].corr(result['Energy Supply per Capita'], method = 'pearson')

ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
				  
result.reset_index(inplace = True)
result['Continent'] = result['Country'].map(ContinentDict)#sum, mean, and std deviation
t = result.groupby(['Continent'])['pop'].agg({'size': np.size, 'sum' : np.sum, 'mean' : np.mean, 'std' : np.std})


result['PopEst'] = (result['Energy Supply'] / result['Energy Supply per Capita']).map('{:,}'.format)



bins = pd.cut(result['% Renewable'], 5)
res = result.groupby(['Continent',bins])['Country'].agg({'size': np.size}).squeeze()
res