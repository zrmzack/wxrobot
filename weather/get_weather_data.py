import requests
from weather.key_weather import KEY

''' official website  https://www.qweather.com '''
'''      dev website  https://dev.qweather.com'''
mykey = '&key=' + KEY  # EDIT HERE!

url_api_weather = 'https://devapi.qweather.com/v7/weather/'
url_api_geo = 'https://geoapi.qweather.com/v2/city/'
url_api_rain = 'https://devapi.qweather.com/v7/minutely/5m'
url_api_air = 'https://devapi.qweather.com/v7/air/now'


def get(api_type, city_id):
    url = url_api_weather + api_type + '?location=' + city_id + mykey
    return requests.get(url).json()


def rain(lat, lon):
    url = url_api_rain + '?location=' + lat + ',' + lon + mykey
    return requests.get(url).json()


def air(city_id):
    url = url_api_air + '?location=' + city_id + mykey
    return requests.get(url).json()


def get_city(city_kw):
    url_v2 = url_api_geo + 'lookup?location=' + city_kw + mykey
    city = requests.get(url_v2).json()['location'][0]

    city_id = city['id']
    district_name = city['name']
    city_name = city['adm2']
    province_name = city['adm1']
    country_name = city['country']
    lat = city['lat']
    lon = city['lon']

    return city_id, district_name, city_name, province_name, country_name, lat, lon


def init(info):
    city_idname = get_city(info)
    city_id = city_idname[0]
    get_now = get('now', city_id)
    get_daily = get('3d', city_id)  # 3d/7d/10d/15d
    get_hourly = get('24h', city_id)  # 24h/72h/168h
    get_rain = rain(city_idname[5], city_idname[6])  # input longitude & latitude
    air_now = air(city_id)['now']
    c1=''
    c2=''
    c3=''
    all=''
    # print(json.dumps(get_now, sort_keys=True, indent=4))
    if city_idname[2] == city_idname[1]:
        print(city_idname[3], str(city_idname[2]) + '市')
        all=city_idname[3]+' '+str(city_idname[2])+ '市'
    else:

        print(city_idname[3], str(city_idname[2]) + '市', str(city_idname[1]) + '区')
        all=city_idname[3]+str(city_idname[2])+'市'+str(city_idname[1]) + '区'

    tianqi = '当前天气： '+str(get_now['now']['text'])+' '+ str(get_now['now']['temp'])+'°C'+ ' 体感温度: '+ str(get_now['now']['feelsLike'])+'°C'
    kqzl = '空气质量指数：'+str(air_now['aqi'])
    jrtq = '今日天气：'+str(get_daily['daily'][0]['textDay'])+ str(get_daily['daily'][0]['tempMin'])+ '-'+ str(get_daily['daily'][0][
        'tempMax'])+'°C'
    nDaysLater = 1  # future weather daily
    oneday = (str(nDaysLater)+ '天后天气：'+str(get_daily['daily'][nDaysLater]['textDay'])+str(get_daily['daily'][nDaysLater][
        'tempMin'])+ '-'+str(get_daily['daily'][nDaysLater]['tempMax'])+ '°C')
    return all,tianqi, kqzl, jrtq, oneday


# all,tianqi, kqzl, jrtq, oneday = init('浦江')
