import pandas as pd

def get_position():
    data = pd.read_excel('/Users/zhangrunmin/PycharmProjects/wxrobot/weather/position.xlsx')
    data.fillna('北京', inplace=True)
    first_data = set(data['省/自治区'].tolist())
    second_data = set(data['直辖市/市/州'].tolist())
    third_data = set(data['县/市辖区/自治县'].tolist())
    final_data = list()
    for i in first_data:
        final_data.append(i)
    for i in second_data:
        final_data.append(i)
    for i in third_data:
        final_data.append(i)
    final_data = (set(final_data))
    return final_data
