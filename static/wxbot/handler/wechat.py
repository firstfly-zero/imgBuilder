import requests, datetime
import os,time
from config import conf
from common.log import logger
from lib import itchat
from lib.itchat.content import *


# 订阅私聊消息
@itchat.msg_register(TEXT)
def handler_single_msg(msg):
    '''
    :param msg: {'MsgId': '5050955702692243306', 'FromUserName': '@27e2cb58830b3f219b674b37a709906d043af73eb8abbd9acb4b6edee38be521', 'ToUserName': '@e7260977c3645fd22582ad139d7aac4ecf824a6a89f944bda0084f308203ded5', 'MsgType': 1, 'Content': '你好', 'Status': 3, 'ImgStatus': 1, 'CreateTime': 1682610726, 'VoiceLength': 0, 'PlayLength': 0, 'FileName': '', 'FileSize': '', 'MediaId': '', 'Url': '', 'AppMsgType': 0, 'StatusNotifyCode': 0, 'StatusNotifyUserName': '', 'RecommendInfo': {'UserName': '', 'NickName': '', 'QQNum': 0, 'Province': '', 'City': '', 'Content': '', 'Signature': '', 'Alias': '', 'Scene': 0, 'VerifyFlag': 0, 'AttrStatus': 0, 'Sex': 0, 'Ticket': '', 'OpCode': 0}, 'ForwardFlag': 0, 'AppInfo': {'AppID': '', 'Type': 0}, 'HasProductId': 0, 'Ticket': '', 'ImgHeight': 0, 'ImgWidth': 0, 'SubMsgType': 0, 'NewMsgId': 5050955702692243306, 'OriContent': '', 'EncryFileName': '', 'User': <User: {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@27e2cb58830b3f219b674b37a709906d043af73eb8abbd9acb4b6edee38be521', 'NickName': '贾一飞', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=606987151&username=@27e2cb58830b3f219b674b37a709906d043af73eb8abbd9acb4b6edee38be521&skey=@crypt_c0e04a07_fc73bd245e4863b8582c5d0cb61974cf', 'ContactFlag': 3, 'MemberCount': 0, 'RemarkName': '', 'HideInputBarFlag': 0, 'Sex': 1, 'Signature': '该考虑如何使用自己的积累了', 'VerifyFlag': 0, 'OwnerUin': 0, 'PYInitial': 'JYF', 'PYQuanPin': 'jiayifei', 'RemarkPYInitial': '', 'RemarkPYQuanPin': '', 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'AttrStatus': 102757, 'Province': '北京', 'City': '', 'Alias': '', 'SnsFlag': 257, 'UniFriend': 0, 'DisplayName': '', 'ChatRoomId': 0, 'KeyWord': '', 'EncryChatRoomId': '', 'IsOwner': 0}>, 'Type': 'Text', 'Text': '你好'}
    :return: action_list
    '''
    WeixinMjRobot().handler_single_msg(msg)


# 订阅群聊文本消息
@itchat.msg_register(TEXT, isGroupChat=True)
def handler_group_msg(msg):
    WeixinMjRobot().handler_group_text_msg(msg)

# 订阅群聊语音消息
@itchat.msg_register(VOICE, isGroupChat=True)
def handler_group_msg(msg):
    WeixinMjRobot().handler_group_voice_msg(msg)

@itchat.msg_register(PICTURE, isGroupChat=True)
def handler_group_picture_msg(msg):
    WeixinMjRobot().handler_group_picture_msg(msg)


class WeixinMjRobot():
    def __init__(self):
        self.config = conf()

    def start(self):
        itchat.instance.receivingRetryCount = 600  # 修改断线超时时间

        try:
            itchat.auto_login(enableCmdQR=2, hotReload=True)
        except:
            logger.error("Hot reload failed, try to login without hot reload")
            itchat.logout()
            os.remove("itchat.pkl")
            itchat.auto_login(enableCmdQR=2, hotReload=True)

        self.user_id = itchat.instance.storageClass.userName
        self.name = itchat.instance.storageClass.nickName
        logger.info("Wechat login success, user_id: {}, nickname: {}".format(self.user_id, self.name))
        # start message listener
        itchat.run()

    # 群文本消息处理逻辑
    def handler_group_text_msg(self, msg):
        # 白名单检测
        group_name = msg["User"]["NickName"]
        group_name_white_list = self.config.get("group_name_white_list")
        if group_name_white_list != None and 'ALL_GROUP' in group_name_white_list:
            pass
        elif group_name_white_list != None and group_name in group_name_white_list:
            pass
        else:
            return None

        # 通用逻辑
        self.handle_common(msg)

        # 判断是否开启了 mjbot
        if self.config.get("switch_mj"):
            self.handle_mj(msg)
        # 判断是否开启了 sdbot
        if self.config.get("switch_sd"):
            self.handle_sd(msg)
        # 判断是否开启了 gpt
        if self.config.get("switch_gpt"):
            self.handle_gpt(msg)

    # 群图片消息处理逻辑
    def handler_group_picture_msg(self, msg):
        filepath = os.path.join("/tmp", msg.fileName)
        # 下载图片
        msg.download(filepath)
        time.sleep(1)

        with open(filepath, 'rb') as f:
            files = [
                ('file', (msg.fileName, f, 'image/jpeg'))
            ]
            # 上传图片
            requests.request(
                method="POST",
                url="{}/api/v1/robot/uploadWxImage".format(self.config.get("server")),
                headers={
                    'Accept': 'application/json, text/plain, */*',
                },
                data={
                    "from_user": msg['ActualNickName'],
                    "ib_username": self.config.get("ib_username")
                },
                files=files,
            )

    # 群语音消息处理逻辑
    def handler_group_voice_msg(self, msg):
        filepath = os.path.join("/tmp", msg.fileName)
        # 下载语音 todo 将语音文件上传到服务器
        msg.download(filepath)
        time.sleep(1)

        with open(filepath, 'rb') as f:
            files = [
                ('file', (msg.fileName, f, 'audio/mpeg'))
            ]
            # 上传语音
            res = requests.request(
                method="POST",
                url="{}/api/v1/robot/uploadWxVoice".format(self.config.get("server")),
                headers={
                    'Accept': 'application/json, text/plain, */*',
                },
                data={
                    "wx_user_id": msg['FromUserName'],
                    "wx_nickname": msg['ActualNickName'],
                    "wx_bot": itchat.instance.storageClass.userName,
                    "ib_username": self.config.get("ib_username")
                },
                files=files,
            )
            itchat.send(
                res.json()["data"],
                toUserName=msg['FromUserName']
            )

    # 通用消息处理逻辑
    def handle_common(self, msg):
        # 图片上传
        if msg["Content"].startswith("/上传"):
            # 无参数，上传到公共相册中
            move_res = requests.request(
                method="POST",
                url="{}/api/v1/robot/moveWxImageToAlbum".format(self.config.get("server")),
                headers={
                    'Accept': 'application/json, text/plain, */*',
                },
                json={
                    "from_user": msg['ActualNickName'],
                    "album_name": msg["Content"].replace("/上传", "").replace(" ", ""),
                    "ib_username": self.config.get("ib_username")
                },
            )
            itchat.send(
                "{}[月亮]图片 ID：{}\n🔗图片链接：{}\n{}".format(
                    str(move_res.json()["data"]["head_msg"]),
                    str(move_res.json()["data"]["id"]),
                    str(move_res.json()["data"]["url"]),
                    str(move_res.json()["data"]["tail_msg"]),
                ),
                toUserName=msg['FromUserName']
            )

    # 机器人 sd 消息处理逻辑，帮助、文生图、图生图、指令消息
    def handle_sd(self, msg):
        # 帮助
        if msg["Content"].startswith("/帮助"):
            help_text = self.config.get("help_text_sd")
            itchat.send(
                help_text,
                toUserName=msg['FromUserName']
            )
            return None

        # 生图逻辑
        if msg["Content"].startswith("/出图"):
            # sd 图片处理逻辑
            sdtask_res = requests.request(
                method="POST",
                url="{}/api/v1/robot/createWxSdTask".format(self.config.get("server")),
                headers={
                    'Accept': 'application/json',
                },
                json={
                    "wx_msg": msg["Content"].replace("/出图", ""),
                    "wx_user_id": msg['FromUserName'],
                    "wx_nickname": msg['ActualNickName'],
                    "wx_bot": itchat.instance.storageClass.userName,
                    "ib_username": self.config.get("ib_username")
                },
            )
            # 任务创建回应
            itchat.send(
                "{}🚀任务已经创建\n🌟任务 ID：{}\n{}".format(
                    str(sdtask_res.json()["data"]["head_msg"]),
                    str(sdtask_res.json()["data"]["id"]),
                    str(sdtask_res.json()["data"]["tail_msg"]),
                ),
                toUserName=msg['FromUserName']
            )

        return None

    # 机器人 gpt 消息处理逻辑
    def handle_gpt(self, msg):
        # 帮助
        if msg["Content"].startswith("/帮助"):
            help_text = self.config.get("help_text_gpt")
            itchat.send(
                help_text,
                toUserName=msg['FromUserName']
            )
            return None

        # 问答逻辑
        gpt_res = requests.request(
            method="POST",
            url="{}/api/v1/robot/getWxGptMsg".format(self.config.get("server")),
            headers={
                'Accept': 'application/json',
            },
            json={
                "wx_msg": msg["Content"],
                "wx_user_id": msg['FromUserName'],
                "wx_nickname": msg['ActualNickName'],
                "wx_bot": itchat.instance.storageClass.userName,
                "ib_username": self.config.get("ib_username")
            },
        )
        try:
            # 任务创建回应
            itchat.send(
                "{}\n{}\n{}".format(
                    str(gpt_res.json()["data"]["head_msg"]),
                    str(gpt_res.json()["data"]["answer"]),
                    str(gpt_res.json()["data"]["tail_msg"]),
                ),
                toUserName=msg['FromUserName']
            )
        except:
            pass

        return None

    # 机器人 mj 消息处理逻辑，文生图、图生图、指令消息
    def handle_mj(self, msg):
        # 帮助
        if msg["Content"].startswith("/help"):
            help_text = self.config.get("help_text_mj", "")
            itchat.send(
                help_text,
                toUserName=msg['FromUserName']
            )
            return None

        # 生图逻辑
        if msg["Content"].startswith("/imagine"):
            mjtask_res = requests.request(
                method="POST",
                url="{}/api/v1/robot/createWxMjTask".format(self.config.get("server")),
                headers={
                    'Accept': 'application/json',
                },
                json={
                    "wx_msg": msg["Content"],
                    "wx_user_id": msg['FromUserName'],
                    "wx_nickname": msg['ActualNickName'],
                    "wx_bot": itchat.instance.storageClass.userName,
                    "ib_username": self.config.get("ib_username")
                },
            )

            # 任务创建回应
            itchat.send(
                "{}🚀任务已经创建\n🌟任务 ID：{}\n{}".format(
                    str(mjtask_res.json()["data"]["head_msg"]),
                    str(mjtask_res.json()["data"]["id"]),
                    str(mjtask_res.json()["data"]["tail_msg"]),
                ),
                toUserName=msg['FromUserName']
            )

        # 变换逻辑
        if msg["Content"].startswith("/up"):
            up_info = msg["Content"].strip().split(" ")
            if len(up_info) == 3:
                mjtask_res = requests.request(
                    method="POST",
                    url="{}/api/v1/robot/createWxMjTask".format(self.config.get("server")),
                    headers={
                        'Accept': 'application/json',
                    },
                    json={
                        "wx_msg": msg["Content"],
                        "wx_user_id": msg['FromUserName'],
                        "wx_nickname": msg['ActualNickName'],
                        "wx_bot": itchat.instance.storageClass.userName,
                        "ib_username": self.config.get("ib_username")
                    },
                )

                # 任务创建回应
                itchat.send(
                    "{}🚀变换任务已经创建\n🌟任务 ID：{}\n{}".format(
                        str(mjtask_res.json()["data"]["head_msg"]),
                        str(mjtask_res.json()["data"]["id"]),
                        str(mjtask_res.json()["data"]["tail_msg"]),
                    ),
                    toUserName=msg['FromUserName']
                )
            else:
                itchat.send(
                    "@{} \n❌请输入正确的格式哦：/up 任务id 变换类型".format(msg['ActualNickName']),
                    toUserName=msg['FromUserName']
                )
        return None

    # 私聊消息处理逻辑
    def handler_single_msg(self, msg):
        if msg["Content"] == "更新指令":
            self.config = conf()
            logger.info("指令集已更新：{}".format(self.config.get("command_list")))
            itchat.send(
                "指令集已更新：{}".format(self.config.get("command_list")),
                toUserName=msg['FromUserName']
            )
