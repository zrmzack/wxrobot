from corona.ShowapiRequest import ShowapiRequest


def get_csv():
    r = ShowapiRequest("http://route.showapi.com/2217-2", "875263", "cb012808d618499aab1aab3a7c5205e9")
    res = r.post()
    import json
    data = json.loads(res.text)
    provinces = []
    high = []
    mid = []
    for i in data['showapi_res_body']['todayDetailList']:
        if (i['midDangerNum']) != 0 or (i['highDangerNum']) != 0:
            print(i['provinceName'])
            #         print(i['dangerAreas'])
            #         print(type(i['dangerAreas']))
            for j in i['dangerAreas']:
                if j['dangerLevel'] == 1:
                    #                     print('高风险')
                    #                     print(j['areaName'])
                    provinces.append(i['provinceName'])
                    high.append(j['areaName'])
                    mid.append('')
                elif j['dangerLevel'] == 2:
                    #                     print('中风险')
                    #                     print(j['areaName'])
                    provinces.append(i['provinceName'])
                    mid.append(j['areaName'])
                    high.append('')
    import pandas as pd
    data_frame_dict = {'省份': provinces, '高风险': high, '中风险': mid}
    data = pd.DataFrame(data_frame_dict)
    data.to_csv('/Users/zhangrunmin/Desktop/wxrobot/robot/疫情.csv')
    return provinces
get_csv()