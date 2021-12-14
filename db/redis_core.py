import redis
import pandas as pd
from algorithm.algorithm_core import cal_diff_setence_2

# 初始化redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def redis_to_csv(group_name):
    size = r.llen(group_name)
    name = []
    info = []
    for i in range(0, size):
        temp = r.lindex(group_name, i)
        temp_name = temp.split(':')[0]
        temp_info = temp.split(':')[1]
        name.append(temp_name)
        info.append(temp_info)
    dataframe = pd.DataFrame({'name': name, 'info': info})
    return dataframe
# 插入题库
# 插入方式，问题：你好，请问你叫什么？  答案：我叫张润民
def take_Q_S(info):
    # try:
    #     first_index = pattern.search(info).span(0)[1] + 1
    #     tempxx = (info[first_index:])
    #     second_index = tempxx.find('答') + first_index
    #     question = info[first_index:second_index].strip()
    #     answer = info[second_index + 3:].strip()
    #     print(question, answer)
    # except:
    #     print("录入问题出错")
    # return question, answer
    pass

# 数据插入map
def insert_map_data(question, answer):
    r.hset("QandA", question, answer)
    print('问题已经录入成功')
def get_answer(question,name_del):
    redis_list_key = list(r.hgetall("QandA").keys())
    temp='@'+name_del
    print(temp)
    question=question.replace(temp, '')
    print(question)
    answer = cal_diff_setence_2(question, redis_list_key)
    if answer == None:
        return None
    else:
        return r.hget("QandA", answer)

# 删除数据
# def delete_data(info):
#     r.hdel("QandA",info)
#     print('删除成功')

# info store in redis as list
def group_info_store(group_name,info):
    r.rpush(group_name, info)


# export group info
def group_info_export(group_name):
    #     size=r.llen("group_info")
    #     for i in range(0,size):
    #         print(r.lindex("group_info",i))
    dataframe = redis_to_csv(group_name)
    dataframe.to_csv(group_name + '.csv', encoding='utf-8')

# delete group info
def remove_group_info(group_name):
    size = r.llen(group_name)
    for i in range(0, size):
        r.brpop(group_name)

# 处理数据分析问题
def calculate(name):
    dframe = pd.read_excel(name)
    dframe.fillna(0,inplace=True)
    data=dframe[dframe['机房']!=0]
    names_jf=set(data['机房'].tolist())
    names_all_jf=(data['机房'].tolist())
    times=0
    jf=''
    for i in names_jf:
        temp=round(names_all_jf.count(i)/len(names_all_jf),2)
        if(temp>times):
            times=temp
            jf=i
    print(times)
    print(jf)

    return times,jf
