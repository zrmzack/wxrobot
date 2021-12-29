from corona.ShowapiRequest import ShowapiRequest

def get_express_data():
    import pandas as pd
    data=pd.read_csv('express.csv')
    key=data['ExpressAllName']
    express_dict=dict(zip())