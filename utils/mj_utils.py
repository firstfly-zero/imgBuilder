import requests
import json
import pandas as pd
import re

class Sender:
    def __init__(self, authorization, channel_id, application_id, guild_id, session_id, version, id, flags, proxy):
        self.authorization = authorization
        self.channel_id = channel_id
        self.application_id = application_id
        self.guild_id = guild_id
        self.session_id = session_id
        self.version = version
        self.id = id
        self.flags = flags
        self.headers = {
            'authorization': self.authorization
        }
        self.proxies = {'http': 'http://' + proxy, 'https': 'http://' + proxy} if proxy else {}

    def send(self, prompt):
        return requests.post(
            url = 'https://discord.com/api/v9/interactions',
            json = {
                'type': 2,
                'application_id': self.application_id,
                'guild_id': self.guild_id,
                'channel_id': self.channel_id,
                'session_id': self.session_id,
                'data': {
                    'version': self.version,
                    'id': self.id,
                    'name': 'imagine',
                    'type': 1,
                    'options': [{'type': 3, 'name': 'prompt', 'value': str(prompt) + ' ' + self.flags}],
                    'attachments': []}
                },
            headers = self.headers,
            proxies = self.proxies
        )

    def send_UVX(self, message_id, component_type, custom_id):
        print(message_id, component_type, custom_id)
        return requests.post(
            url = 'https://discord.com/api/v9/interactions',
            json = {
                'type': 3,
                'application_id': self.application_id,
                'guild_id': self.guild_id,
                'channel_id': self.channel_id,
                'session_id': self.session_id,
                'message_id': message_id,
                'data': {
                    'component_type': component_type,
                    'custom_id': custom_id
                }
            },
            headers = self.headers,
            proxies = self.proxies
        )

class Receiver:
    def __init__(self, channel_id, authorization, proxy):
        self.df = pd.DataFrame(columns=['prompt', 'task_id', 'url', 'filename', 'is_downloaded', 'mj_done_msg'])
        self.awaiting_list = pd.DataFrame(columns=['prompt', 'task_id', 'status'])
        self.channel_id = channel_id
        self.authorization = authorization
        self.headers = {'authorization': self.authorization}
        self.proxies = {'http': 'http://' + proxy, 'https': 'http://' + proxy} if proxy else {}

    def retrieve_messages(self):
        try:
            r = requests.get(
                url = 'https://discord.com/api/v10/channels/{}/messages?limit=20'.format(self.channel_id),
                headers = self.headers,
                proxies = self.proxies,
                timeout = (5, 10)
            )
            jsonn = json.loads(r.text)
            return jsonn
        except:
            return json.loads("{}")

    def collecting_results(self):
        message_list = self.retrieve_messages()
        for message in message_list:
            print(message)
            try:
                if (message['author']['username'] == 'Midjourney Bot') and ('**' in message['content']):
                    if len(message['attachments']) > 0:
                        # 已完成列表
                        if (message['attachments'][0]['filename'][-4:] == '.png') or (
                                '(Open on website for full quality)' in message['content']):
                            id = message['id']
                            task_id = re.findall("<@\d+>", message['content'])[0].replace("<@", "").replace(">", "")
                            prompt = message['content'].split('**')[1].strip()
                            url = message['attachments'][0]['url']
                            filename = message['attachments'][0]['filename']
                            if id not in self.df.index:
                                self.df.loc[id] = [prompt, task_id, url, filename, 0, message]
                        # 进行中列表
                        else:
                            id = message['id']
                            task_id = re.findall("<@\d+>", message['content'])[0].replace("<@", "").replace(">", "")
                            prompt = message['content'].split('**')[1].split('--')[0].strip()
                            status = 'unknown status'
                            if ('(fast)' in message['content']) or ('(relaxed)' in message['content']):
                                try:
                                    status = re.findall("(\w*%)", message['content'])[0]
                                except:
                                    status = 'unknown status'
                            self.awaiting_list.loc[id] = [prompt, task_id, status]

                    else:
                        id = message['id']
                        task_id = re.findall("<@\d+>", message['content'])[0].replace("<@", "").replace(">", "")
                        prompt = message['content'].split('**')[1].split('--')[0].strip()
                        status = 'unknown status'
                        if '(Waiting to start)' in message['content']:
                            status = 'Waiting to start'
                        self.awaiting_list.loc[id] = [prompt, task_id, status]
            except:
                continue
