dates = []
doc = []
with open('dates.txt') as file:
    for line in file:
        doc.append(line)

df = pd.Series(doc)

def init_regex():
        regex = ['(?P<month>\d{1,2})[/-]+(?P<day>\d{1,2})[/-]+(?P<year>\d{2,4})',
        '(?P<month>jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*(?:,|-|\.|\s|\.{,2})+(?P<day>\d{1,2})[-,\s]+(?P<year>\d{2,4})+',
        '(?P<day>\d{1,2})[\s]?(?P<month>jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*(?:\s|.{,2})(?P<year>\d{2,4})',
        '(?P<month>jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)+[\s]+(?P<day>\d{1,2})(?:th|st|nd)*[,\s]+(?P<year>\d{2,4})+',
        '(?P<month>jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*(?:,|\s|\.{,2})+(?P<year>\d{2,4})',
        '(?P<month>\d{1,2})/(?P<year>\d{2,4})+',
        '(?P<year>\d{4})']
        
        return regex


def extract_date(row, dates_regex):
    from datetime import datetime
    months_dic = {'jan' : 1, 'feb' : 2, 'mar' : 3, 'apr' : 4, 'may' : 5, 'jun' : 6, 'jul' : 7, 'aug' : 8,
                  'sep' : 9, 'oct' : 10, 'nov' : 11, 'dec' : 12}
    res_ = None
    for regex in dates_regex:
        res_ = regex.search(str(row).lower())
        if res_:
            break

    if not res_:
        return None
    
    day, month, year = 1, 1, 1900
    if len(res_.groups()) == 3:
        month, day, year = res_.group('month'), res_.group('day'), res_.group('year')
    elif len(res_.groups()) == 2:
        month, year = res_.group('month'), res_.group('year')
    else:
        year = res_.group('year')
    
    if type(day) is not int:
        day = int(day)
    
    if type(month) is not int:
        month = int(month) if month.isdigit() else months_dic[month]
    
    if len(year) <= 2:
        year = int(year) + 1900
    else:
        year = int(year)
    
    if day > 31 or month > 12 or day == 0 or month == 0 or year < 1900:
        return None
    
    return datetime(year=int(year), month=int(month), day=int(day))

def date_sorter():
    import re
    pegex = init_regex()
    
    dates = []
    dates.append(re.compile(pegex[0]))
    dates.append(re.compile(pegex[1]))
    dates.append(re.compile(pegex[2]))
    dates.append(re.compile(pegex[3]))
    dates.append(re.compile(pegex[4]))
    dates.append(re.compile(pegex[5]))
    dates.append(re.compile(pegex[6]))
    
    df_dates = df.apply(extract_date, args=(dates,))
    
    indx_values = range(0, len(df_dates))
    df_dates = pd.DataFrame(index = indx_values, data = df_dates, columns=['date'])

    df_dates.sort_values(by='date', inplace = True)

    return df_dates