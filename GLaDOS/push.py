import requests
from logger import logger

def send_msg_ServerChan(SendKey, title, msg):
    if not SendKey:
        return 'Sever酱: 未配置SendKey，无法进行消息推送.'

    logger.info('========================================')
    logger.info('Sever酱: 开始推送消息！')

    url = f'https://sctapi.ftqq.com/{SendKey}.send'
    data = {'title': title, 'desp': msg, 'channel': 9}
    rsp = requests.post(url, data=data)
    pushid = rsp.json()['data']['pushid']
    readkey = rsp.json()['data']['readkey']
    state_url = f'https://sctapi.ftqq.com/push?id={pushid}&readkey={readkey}'

    count = 1
    while True:
        status_rsp = requests.get(state_url)
        result = status_rsp.json()['data']['wxstatus']
        logger.info(f'查询消息推送是否成功：{count}')

        if result:
            return '消息推送成功！'
        elif count >= 60:   # 防止程序一直运行
            return '程序运行结束！推送结果未知！'
        count += 1
        time.sleep(1)

def send_msg_PushPlus(token, title, msg):
    if not token:
        return 'PushPlus: 未配置token，无法进行消息推送.'

    logger.info('========================================')
    logger.info('PushPlus: 开始推送消息！')

    url = 'http://www.pushplus.plus/send/'
    headers = {'Content-Type': 'application/json'}
    data = {
        "token": token,
        "title": title,
        "content": msg,
        "template": "txt",
        "channel": "wechat"
    }
    rsp = requests.post(url=url, json=data, headers=headers)
    return rsp.json()['msg']

def send_msg_WxPusher(appToken, uids, title, msg):
    if not (appToken and uids):
        return 'WxPusher: 未配置appToken和uids，无法进行消息推送.'

    logger.info('========================================')
    logger.info('WxPusher: 开始推送消息！')

    url = 'https://wxpusher.zjiecode.com/api/send/message'
    headers = {'Content-Type': 'application/json'}

    data = {
        "appToken": appToken,
        "content": msg,
        "summary": title,
        "contentType": 1,
        "uids": [uids]
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()

        if response_data.get('code') == 1000:
            return 'WxPusher: 消息推送成功！'
        else:
            return f'WxPusher: 消息推送失败 - {response_data.get("msg")}'
    except Exception as e:
        return f'WxPusher: 消息推送失败 - {str(e)}'

def send_msg_Qmsg(key, msg):
    if not key:
        return 'Qmsg: 未配置key，无法进行消息推送.'

    logger.info('========================================')
    logger.info('Qmsg: 开始推送消息！')

    url = f'https://qmsg.zendee.cn:443/send/{key}'
    params = {'msg': msg}
    rsp = requests.get(url=url, params=params).json()

    if rsp and rsp['success']:
        return 'Qmsg: 消息推送成功！'
    return 'Qmsg: 消息推送失败！'
