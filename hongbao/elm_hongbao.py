def get_elm():
    import requests
    url = "http://api.web.ecapi.cn/taoke/getTbkActivityInfo?"
    params = {
        "apkey": "63bd80ea-6388-5583-2142-e3e05941c601",
        "tbname": "欢民123",
        "pid": "mm_812090041_1187450424_109888350204",
        "activity_material_id": "20150318020002597",
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }
    res = requests.request('GET', url, params=params, headers=headers)

    import json
    data = json.loads(res.text)
    return data['data']['short_click_url']

