from corona.ShowapiRequest import ShowapiRequest

r = ShowapiRequest("http://route.showapi.com/2217-2", "875263", "cb012808d618499aab1aab3a7c5205e9")
res = r.post()
print(res.text)
