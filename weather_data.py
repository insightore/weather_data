# 2017-08-18 23:00AM to 2018-08-19 04:06AM
# weather_data
# ###################
# imports
# ###################

import requests
import json
from datetime import date
import pandas as pd
import numpy as np

# ###################
# Get today's weather forecast
# ###################

# sample code
# http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID={APIKEY}

city = "London"
country_code = "UK"
location = city+','+country_code
APIKEY = '##########' #get an api key from openweathermap.org
url = "http://api.openweathermap.org/data/2.5/find?q=%s&units=metric&APPID=%s" %(location,APIKEY)
# headers = {"Authorization":"Bearer %s"%key}

response = requests.get(url)
response_dict = json.loads(response.text)
# response_dict

# for index, item in enumerate(response_dict['list'][0]): print (index, item, '\n')
london_uk_today = response_dict['list'][0]
print ("Today's date is",date.today())
print("The average temperature today is", str(london_uk_today['main']['temp'])+"˚C."\
      , "You should expect", str(london_uk_today['weather'][0]['description'])+".")  
# this part took an hour to develop

# ###################
# Get 5 day forecast
# ###################

# sample api "http://api.openweathermap.org/data/2.5/forecast?q={city name},{country code}"
url = "http://api.openweathermap.org/data/2.5/forecast?q=%s&APPID=%s&units=metric" %(location,APIKEY)
response = requests.get(url)
response_dict = json.loads(response.text)
# response_dict

# response_dict['list']
date_time = []
temp_deg_c = []
date=[]
for index, item in enumerate(response_dict['list']):
    date_time.append (response_dict['list'][index]['dt_txt'])
    temp_deg_c.append (response_dict['list'][index]['main']['temp'])
time=list(map(lambda x : str(x).split(" ")[1], (response_dict['list'][index]['dt_txt'] for index, item in enumerate(response_dict['list']))))
date=list(map(lambda x : str(x).split(" ")[0], (response_dict['list'][index]['dt_txt'] for index, item in enumerate(response_dict['list']))))
temp_c_rounded=list(map(lambda x : (round(x,0)), (response_dict['list'][index]['main']['temp'] for index, item in enumerate(response_dict['list']))))


s_date_time = pd.Series(data = date_time)
s_temp_deg_c = pd.Series(data =  temp_deg_c)
forecast_5d = pd.DataFrame(data ={"date_time":s_date_time,"temp_deg_c":s_temp_deg_c, "date": date, 'time':time, 'temp_c_rounded':temp_c_rounded})
# print ('forecast for every 3 hours for the next 5 days in %s', forecast_5d %location)
print('\n','################')
print('Here is the forecast for every 3 hours for the next 5 days in %s' %location.replace(',',', '))
print(forecast_5d)

avg_5day_test=forecast_5d.groupby(['date'])
test = avg_5day_test.aggregate(np.mean) #.set_index([[i for i in range(0,len(avg_5day_test))]])
test['date']=test.index
test.set_index([[i for i in range(0,len(avg_5day_test))]], inplace=True)
print('\n','################')
print (test)

grouped = forecast_5d.groupby(['date'],as_index=False)
avg_5day = grouped.aggregate(np.mean)
avg_5day.temp_c_rounded=round(avg_5day.temp_c_rounded,0).astype('int')
print('\n','################')
print('the average daily forecast for the next 5 days')
print (avg_5day)

# 4h43m45s09 --> The amount of time it took me to get the total code above. A lot of the time was spent learning new ways of doing things in python such as lambda for functions.





