import requests
from requests_toolbelt import MultipartEncoder

class LarkRobot():
    # 构造函数
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        # 获取authorization
        try:
            response = requests.request(
                method="POST",
                url='https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/',
                json={
                    "app_id": self.app_id,
                    "app_secret": self.app_secret,
                }
            )
            self.authorization = "Bearer " + response.json()["tenant_access_token"]
        except:
            pass

    def sendRichtextToChat(self, chat_id, rich_text):
        # 发送富文本信息到chat_id对应的群聊
        res = requests.request(
            method="POST",
            url="https://open.feishu.cn/open-apis/message/v4/send/",
            headers={"Authorization": self.authorization, "Content-Type": "application/json"},
            json={"chat_id": chat_id, "msg_type": "post", "content": {"post": {"zh_cn": rich_text}}}
        )
        return res.json()

    def sendRichtextToChatByEmail(self, email, rich_text):
        # 发送富文本信息到chat_id对应的群聊
        res = requests.request(
            method="POST",
            url="https://open.feishu.cn/open-apis/message/v4/send/",
            headers={"Authorization": self.authorization, "Content-Type": "application/json"},
            json={"email": email, "msg_type": "post", "content": {"post": {"zh_cn": rich_text}}}
        )
        return res.json()

    def sendCardToChat(self, chat_id, card):
        # 发送卡片信息到chat_id对应的群聊
        res = requests.request(
            method="POST",
            url="https://open.feishu.cn/open-apis/message/v4/send/",
            headers={"Authorization": self.authorization, "Content-Type": "application/json"},
            json={"chat_id": chat_id, "MsgType": "interactive", "msg_type": "interactive", "card": card}
        )
        return res.json()

    def getUserinfo(self, open_id):
        # 根据openid获取用户信息
        res = requests.request(
            method="GET",
            # url="https://open.feishu.cn/open-apis/user/v4/info?open_id="+open_id,
            url="https://open.feishu.cn/open-apis/contact/v3/users/" + open_id,
            headers={"Authorization": self.authorization, "Content-Type": "application/json"},
        )
        return res.json()["data"]

    def inviteUserToChat(self, chat_id, open_id_list):
        # 邀请用户进群
        res = requests.request(
            method="POST",
            url="https://open.feishu.cn/open-apis/chat/v4/chatter/add/",
            headers={"Authorization": self.authorization, "Content-Type": "application/json"},
            json={"chat_id": chat_id, "open_ids": open_id_list}
        )
        return res.json()

    def createChat(self, name, desc, open_ids):
        # 创建群聊
        res = requests.request(
            method="POST",
            url="https://open.feishu.cn/open-apis/chat/v4/create/",
            headers={"Authorization": self.authorization, "Content-Type": "application/json"},
            json={"name": name, "description": desc, "open_ids": open_ids}
        )
        return res.json()

    def getId(self, email):
        # 创建群聊
        # @params email 用户信息中定义的邮箱，例如jiayifei@bytedance.com
        # @return {'open_id': 'ou_29afc01d3cee4d14afa2b182bf667758', 'user_id': 'd2bbc6f2'}
        res = requests.request(
            method="POST",
            url="https://open.feishu.cn/open-apis/user/v4/email2id",
            headers={"Authorization": self.authorization, "Content-Type": "application/json"},
            json={"email": email}
        )
        return res.json()["data"]

    def uploadImage(self,filepath):
        form = {
            'image_type': 'message',
            'image': (open(filepath, 'rb'))
        }
        multi_form = MultipartEncoder(form)
        res = requests.request(
            method="POST",
            url="https://open.feishu.cn/open-apis/im/v1/images",
            headers={"Authorization": self.authorization, "Content-Type": multi_form.content_type},
            data=multi_form
        )
        return res.json()

    def uploadAudio(self, filename, duration, filepath):
        form = {
            'file_type': 'opus',
            'file_name': filename,
            'duration': duration,
            'file': (open(filepath, 'rb'))
        }

        multi_form = MultipartEncoder(form)
        res = requests.request(
            method="POST",
            url="https://open.feishu.cn/open-apis/im/v1/files",
            headers={
                "Authorization": self.authorization,
                "Content-Type": multi_form.content_type
            },
            data=multi_form
        )

        return res.json()

    def sendAudioToChat(self, file_key, chat_id):
        import json
        # 获取消息中的文件资源
        res = requests.request(
            method="POST",
            url="https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id",
            headers={"Authorization": self.authorization, "Content-Type": "application/json"},
            json={
                "receive_id": chat_id,
                "content": json.dumps(
                    {
                        "file_key": file_key
                    }
                ),
                "msg_type": "audio",
            }
        )
        return res.json()

    def getMessageImage(self, message_id, file_key):
        # 获取消息中的文件资源
        res = requests.request(
            method="GET",
            url="https://open.feishu.cn/open-apis/im/v1/messages/{}/resources/{}?type=image".format(message_id, file_key),
            headers={"Authorization": self.authorization, "Content-Type": "application/json"},
        )
        return res

    def getMessageAudio(self, message_id, file_key):
        # 获取消息中的文件资源
        res = requests.request(
            method="GET",
            url="https://open.feishu.cn/open-apis/im/v1/messages/{}/resources/{}?type=file".format(message_id, file_key),
            headers={"Authorization": self.authorization, "Content-Type": "application/json"},
        )
        return res
