from hongbao.elm_hongbao import get_elm
from hongbao.mt_hongbao import get_meituan


def set_mt_key():
    import redis
    r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
    if r.get("mt_hb") == None:
        r.set("mt_hb", get_meituan())
        r.expire("mt_hb", time=3600 * 5)
        print('已经重新获取')
        return (r.get("mt_hb"))
    else:
        return (r.get("mt_hb"))

def set_elm_key():
    import redis
    r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
    if r.get("elm_hb") == None:
        r.set("elm_hb", get_elm())
        r.expire("elm_hb", time=3600 * 5)
        print('已经重新获取')
        return (r.get("elm_hb"))
    else:
        return (r.get("elm_hb"))
# print(set_elm_key())
# print(set_mt_key())