from os import environ
from logger import logger
from Check import CheckIn
from push import send_msg_ServerChan, send_msg_PushPlus, send_msg_Qmsg, send_msg_WxPusher

def main():
    # 从环境变量中获取配置信息
    ck = environ.get("cookie")
    SendKey = environ.get("SendKey")
    is_ServerChan_push = int(environ.get("is_ServerChan_push", 0))
    token = environ.get("token")
    is_PushPlus_push = int(environ.get("is_PushPlus_push", 0))
    key = environ.get("key")
    is_Qmsg_push = int(environ.get("is_Qmsg_push", 0))
    appToken = environ.get("appToken")
    uids = environ.get("uid")

    # 检查是否存在cookie配置
    if not ck:
        logger.info("请先配置GLADOS_COOKIE！")
        return

    try:
        # 进行签到操作
        title, msg = CheckIn(ck)
        logger.info("GLaDOS 签到成功！")
    except Exception as err:
        logger.error("程序运行出错！")
        title = "程序运行出错！"
        msg = str(err)
    finally:
        # 按行输出签到信息
        tmp = msg.split("\n")
        for i in tmp:
            logger.info(i)

        # 根据配置向不同平台推送签到信息
        if is_ServerChan_push and SendKey:
            rsp1 = send_msg_ServerChan(SendKey, title, msg)
            logger.info(rsp1)
        if is_PushPlus_push and token:
            rsp2 = send_msg_PushPlus(token, title, msg)
            logger.info(rsp2)
        if is_Qmsg_push and key:
            rsp3 = send_msg_Qmsg(key, msg)
            logger.info(rsp3)
        if appToken and uids:
            rsp4 = send_msg_WxPusher(appToken, uids, title, msg)
            logger.info(rsp4)

if __name__ == "__main__":
    main()
