import requests

class ChatGpt:
    def __init__(self, base_url, api_key, system_message=None, open_history=False, model="gpt-3.5-turbo", proxy=None):
        self.base_url = base_url
        self.api_key = api_key
        self.proxy = proxy
        self.model = model
        self.messages = []
        if system_message is None:
            system_message = {"role": "system", "content": "你是小图，旨在回答人们的问题！"}
        self.messages.append(system_message)
        self.open_history = open_history

    # 传入格式：{"role": "user", "content": "你叫什么名字？"}
    def chatCompletions(self, message):
        if self.open_history:
            if len(self.messages) > 10:
                del self.messages[1]
            self.messages.append(message)
            res = requests.request(
                method="POST",
                url="{}/v1/chat/completions".format(self.base_url),
                headers={"Authorization": "Bearer {}".format(self.api_key), "Content-Type": "application/json"},
                json={
                    "model": self.model,
                    "messages": self.messages
                }
            )
            self.messages.append(res.json()["choices"][0]["message"])
            print(res.json())
            return res.json()["choices"][0]["message"]["content"]
        else:
            self.messages.append(message)
            res = requests.request(
                method="POST",
                url="{}/v1/chat/completions".format(self.base_url),
                headers={"Authorization": "Bearer {}".format(self.api_key), "Content-Type": "application/json"},
                json={
                    "model": self.model,
                    "messages": self.messages
                }
            )
            self.messages.remove(message)
            print(res.json())
            return res.json()["choices"][0]["message"]["content"]

    # 讲语音
    def audioSpeech(self, text, audiopath):
        response = requests.request(
            method="POST",
            url="{}/audio/speech".format(self.base_url),
            headers={"Authorization": "Bearer {}".format(self.api_key), "Content-Type": "application/json"},
            json={
              "model": "tts-1",
              "input": text,
              "voice": "alloy",
              "response_format": "opus"
            }
        )

        with open(audiopath, "wb") as f:
            f.write(response.content)

    # todo 画图