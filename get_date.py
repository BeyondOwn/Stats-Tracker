from datetime import date
from datetime import timedelta
import re

def main():
    get_date_range()

def get_date_range(start_date_input,end_date_input):
    date_arr = []

    ## Input Validation Start Date
    date_wrong1 = re.search(r'^([0-9]{1})\.?\-?([0-9]*)\.?\-?([0-9]{4})$',str(start_date_input))
    if date_wrong1:
        start_date_input = f'0{date_wrong1.group(1)}.{date_wrong1.group(2)}.{date_wrong1.group(3)}'
    date_wrong2 = re.search(r'^([0-9]{2})\.?\-?([0-9]{1})\.?\-?([0-9]{4})$',str(start_date_input))
    if date_wrong2:
        start_date_input = f'{date_wrong2.group(1)}.0{date_wrong2.group(2)}.{date_wrong2.group(3)}'
    ## Input Validation End Date
    date_wrong3 = re.search(r'^([0-9]{1})\.?\-?([0-9]*)\.?\-?([0-9]{4})$',str(end_date_input))
    if date_wrong3:
        end_date_input = f'0{date_wrong3.group(1)}.{date_wrong3.group(2)}.{date_wrong3.group(3)}'
    date_wrong4 = re.search(r'^([0-9]{2})\.?\-?([0-9]{1})\.?\-?([0-9]{4})$',str(end_date_input))
    if date_wrong4:
        end_date_input = f'{date_wrong4.group(1)}.0{date_wrong4.group(2)}.{date_wrong4.group(3)}'
    ##Making normal Date to ISO Format YYYY-MM-DD

    start_day, start_month, start_year = start_date_input.strip().split('.')
    end_day, end_month, end_year = end_date_input.strip().split('.')
    start_date_input = f"{start_year}-{start_month}-{start_day}"
    end_date_input = f"{end_year}-{end_month}-{end_day}"
    
  

    start_date = date.fromisoformat(start_date_input) 
    end_date = date.fromisoformat(end_date_input)    # maybe date.now()

    delta = end_date - start_date   # returns timedelta
    
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        date_arr.append(day.strftime("%d.%m.%Y"))
    

    return date_arr



if __name__ == "__main__":
    main()