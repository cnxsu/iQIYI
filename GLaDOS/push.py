import requests
import time
from logger import logger

def send_msg_ServerChan(SendKey, title, msg):
    if not SendKey:
        return 'Server酱: 未配置SendKey，无法进行消息推送.'

    logger.info('========================================')
    logger.info('Server酱: 开始推送消息！')

    url = f'https://sctapi.ftqq.com/{SendKey}.send'
    data = {'title': title, 'desp': msg, 'channel': 9}
    rsp = requests.post(url, data=data)
    pushid = rsp.json().get('data', {}).get('pushid')
    readkey = rsp.json().get('data', {}).get('readkey')
    state_url = f'https://sctapi.ftqq.com/push?id={pushid}&readkey={readkey}'

    count = 1
    while count <= 60:  # Limit the maximum count
        status_rsp = requests.get(state_url)
        result = status_rsp.json().get('data', {}).get('wxstatus')
        logger.info(f'查询消息推送是否成功：{count}')

        if result:
            return '消息推送成功！'

        count += 1
        time.sleep(1)

    return '程序运行结束！推送结果未知！'

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

    return rsp.json().get('msg')

def send_msg_PushPlusWebhook(token, channel, webhook, title, msg):
    if not (token and channel and webhook):
        return 'PushPlusWebhook: 未配置token and channel and webhook，无法进行消息推送.'

    logger.info('========================================')
    logger.info('PushPlusWebhook: 开始推送消息！')

    url = 'http://www.pushplus.plus/send/'
    headers = {'Content-Type': 'application/json'}
    data = {
        "token": token,
        "title": title,
        "content": msg,
        "template": "txt",
        "channel": channel,
        "webhook": webhook
    }
    rsp = requests.post(url=url, json=data, headers=headers)

    return rsp.json().get('msg')

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

    url = f'https://qmsg.zendee.cn/send/{key}'
    params = {'msg': msg}
    rsp = requests.get(url=url, params=params).json()

    if rsp.get('success', False):
        return 'Qmsg: 消息推送成功!'
    return 'Qmsg: 消息推送失败!'
