from corona.ShowapiRequest import ShowapiRequest


def get_express_data(company, express_id, phone):
    import pandas as pd
    data = pd.read_csv('/Users/zhangrunmin/Desktop/wxrobot/kuaidi/express.csv')
    key = data['ExpressAllName'].tolist()
    value = data['ExpressSimpleName'].tolist()
    express_dict = dict(zip(key, value))
    for i in express_dict.keys():
        if company in i:
            company = express_dict[i]
            break


    r = ShowapiRequest("http://route.showapi.com/64-19", "875263", "cb012808d618499aab1aab3a7c5205e9")
    r.addBodyPara("com", company)
    r.addBodyPara("nu", express_id)
    r.addBodyPara("phone", phone)
    res = r.post()
    info = ''
    import json
    data = json.loads(res.text)
    if data['showapi_res_body']['status'] == 1:
        info = "暂无记录" + '\n'
    if data['showapi_res_body']['status'] == 2:
        info = "在途中" + '\n'
    if data['showapi_res_body']['status'] == 3:
        info = "派送中" + '\n'
    if data['showapi_res_body']['status'] == 4:
        info = '已签收 (完结状态)' + '\n'
    if data['showapi_res_body']['status'] == 5:
        info = '用户拒签' + '\n'
    if data['showapi_res_body']['status'] == 6:
        info = '疑难件' + '\n'
    if data['showapi_res_body']['status'] == 7:
        info = '无效单 (完结状态)' + '\n'
    if data['showapi_res_body']['status'] == 8:
        info = '超时单' + '\n'
    if data['showapi_res_body']['status'] == 9:
        info = '签收失败' + '\n'
    if data['showapi_res_body']['status'] == 10:
        info = '退回' + '\n'
    if data['showapi_res_body']['status'] != 1:
        temp = ''
        for i in data['showapi_res_body']['data']:
            temp += (str(i['time']) + '   ' + str(i['context']) + '\n')
            # print(i['time'], '   ', i['context'])
    return (info + temp)
