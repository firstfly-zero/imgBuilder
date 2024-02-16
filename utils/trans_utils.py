import requests

class BaiduTranslate():
    def __init__(self, appId, apiKey, secretKey):
        # 创建AcsClient实例
        self.appId = appId
        self.apiKey = apiKey
        self.secretKey = secretKey

        response = requests.request(
            method = "POST",
            url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}".format(self.apiKey, self.secretKey),
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )
        self.access_token = response.json().get('access_token')

    # 翻译方法
    def translate(self, text):
        res = requests.request(
            method = "POST",
            url = 'https://aip.baidubce.com/rpc/2.0/mt/texttrans/v1?access_token={}'.format(self.access_token),
            headers = {'Content-Type': 'application/json'},
            json = {'q': text, 'from': 'auto', 'to': 'en', 'termIds': ''}
        )

        return res.json()
