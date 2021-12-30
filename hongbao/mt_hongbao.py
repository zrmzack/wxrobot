def get_meituan():
    url = "http://api.web.ecapi.cn/platform/meituan_v2?&eid=zhangrunmin"
    import requests

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }
    res = requests.request('GET', url, params={'apkey': "63bd80ea-6388-5583-2142-e3e05941c601"}, headers=headers)
    import json
    data = json.loads(res.text)
    return data['data']['url']
