from wxpy import *

from corona.get_corona import get_csv
from db.redis_core import group_info_store, get_answer, group_info_export, calculate
from hongbao.get_hongbao import set_elm_key, set_mt_key
from kuaidi.get_kd import get_express_data
from travel.get_map import generate_map
from weather.position import get_position
from weather.get_weather_data import init


def init_robot():
    # 短时间内免登录，未设置
    # todo
    bot = Bot(cache_path=True)
    bot.enable_puid('wxpy_puid.pkl')
    return bot


def is_express_info(string):
    count = 0
    for i in string:
        if i.isdigit():
            count += 1
    return count > 10


def get_index(data):
    infos = data.split(" ")
    return len(infos)


def get_all_express_info(data):
    infos = data.split(" ")
    company = infos[0].strip()
    exprss_id = infos[1].strip()
    if len(infos) == 2:
        return company, exprss_id
    else:
        phone = infos[2].strip()

    return company, exprss_id, phone


bot = init_robot()


# 获取所有用户信息
def get_all_friends():
    return bot.friends()


# 获取所有群聊消息
def get_all_groups():
    return bot.groups()


position = get_position()


# 处理群聊消息
def group_deal():
    @bot.register(Group, TEXT)
    def group_info(msg):
        # 获取当前群聊名字
        group_name = msg.sender.name
        # 获取当前发送者名字
        send_name = msg.member.name
        # 获取当前发送的信息内容
        send_info = msg.text
        # 转化成可识别形式
        send_info_str = str(send_name) + ":" + str(send_info)
        # 存储到redis
        group_info_store(group_name, send_info_str)
        print('聊天记录存储成功')
        # 如果被选中就需要回答问题了
        if msg.is_at:
            # 自动回复
            if '导出聊天记录' in send_info:
                print('-------------导出中---------------')
                group_info_export(group_name)
                msg.chat.send_file(group_name + '.csv')
                print('-------------导出完成-------------')
            elif '天气' in send_info:
                if '明天天气' in send_info or '今天天气' in send_info:
                    all, tianqi, kqzl, jrtq, oneday = init('北京')
                    # msg.chat.send(all)
                    msg.chat.send(tianqi + '\n' + kqzl + '\n' + jrtq + '\n' + oneday)
                    myself_name = bot.self.name
                    myself_info = str(myself_name) + ":" + str(tianqi + '\n' + kqzl + '\n' + jrtq + '\n' + oneday)
                    group_info_store(group_name, myself_info)
                    # msg.chat.send(kqzl)
                    # msg.chat.send(jrtq)
                    # msg.chat.send(oneday)
                else:
                    city = ''
                    for i in position:
                        if i in send_info:
                            all, tianqi, kqzl, jrtq, oneday = init(i)
                            # msg.chat.send(all)
                            msg.chat.send(tianqi + '\n' + kqzl + '\n' + jrtq + '\n' + oneday)
                            myself_name = bot.self.name
                            myself_info = str(myself_name) + ":" + str(
                                tianqi + '\n' + kqzl + '\n' + jrtq + '\n' + oneday)
                            group_info_store(group_name, myself_info)
                            # msg.chat.send(kqzl)
                            # msg.chat.send(jrtq)
                            # msg.chat.send(oneday)
                            city = all
                            break
                    if (city == ''):
                        msg.chat.send('该地区找不到,试试看加上县或者市吧')
                        myself_name = bot.self.name
                        myself_info = str(myself_name) + ":" + str('该地区找不到,试试看加上县，市或者省')
                        group_info_store(group_name, myself_info)

            elif (get_answer(send_info[:], bot.self.name) == None):
                a = '换个问题吧'
                msg.chat.send(a)
                myself_name = bot.self.name
                myself_info = str(myself_name) + ":" + str(a)
                group_info_store(group_name, myself_info)

            else:
                a = get_answer(send_info[:], bot.self.name)
                msg.chat.send(a)
                #         print(bot.self.name)
                myself_name = bot.self.name
                myself_info = str(myself_name) + ":" + str(a)
                group_info_store(group_name, myself_info)


def friend_deal():
    my_friend = bot.friends()

    # 处理聊天人消息
    @bot.register(my_friend)
    def reply_my_friend(msg):
        #     msg.get_file(msg.get)
        if msg.type == 'Attachment':
            msg.get_file(msg.file_name)
            msg.chat.send(msg.file_name + '文件接收完成')
            x, y = calculate(msg.file_name)
            msg.chat.send('数据解析完成')
            string = str('最有可能出现问题机房:  ') + str(y) + '  发生概率是:  ' + str(x)
            msg.chat.send(string)
        if '疫情信息' in msg.text:
            cor = get_csv()
            string = ''
            for i in set(cor):
                string += str(i) + ' '
            msg.chat.send('目前疫情区域：' + string)
        if '疫情详情' in msg.text:
            get_csv()
            msg.chat.send_file('疫情.csv')
        if '旅游' in msg.text:
            data_pos = get_position()
            ll = []
            for i in data_pos:
                print(i)
                if i in msg.text:
                    ll.append(i)
            generate_map(ll)
            msg.chat.send_file('travel.html')
        if '饿了么红包' in msg.text:
            elm_hongbao = set_elm_key()
            msg.chat.send(elm_hongbao)
        if '美团红包' in msg.text:
            mt_hongbao = set_mt_key()
            msg.chat.send(mt_hongbao)
        if is_express_info(msg.text):
            # print(msg.text)
            if get_index(msg.text) == 3:
                company, exprss_id, phone = get_all_express_info(msg.text)
                # print(phone)
                # print(company)
                # print(exprss_id)
                info = get_express_data(str(company), str(exprss_id), str(phone))
                print(info)
                msg.chat.send(info)

            if get_index(msg.text) == 2:
                company, exprss_id = get_all_express_info(msg.text)
                info = get_express_data(company, exprss_id, "")
                msg.chat.send(info)


if __name__ == '__main__':
    group_deal()
    friend_deal()
    bot.join()
