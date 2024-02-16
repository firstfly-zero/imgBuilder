import requests, time
while True:
    try:
        time.sleep(3)
        wx_sd_res = requests.request(
            method="GET",
            url="http://127.0.0.1:8000/api/v1/robot/executeWxSdTask"
        )
        print(wx_sd_res.text)
        time.sleep(3)
        wx_mj_res = requests.request(
            method="GET",
            url="http://127.0.0.1:8000/api/v1/robot/executeWxMjTask"
        )
        print(wx_mj_res.text)
        time.sleep(3)
        fs_mj_res = requests.request(
            method="GET",
            url="http://127.0.0.1:8000/api/v1/robot/executeWxMjTask"
        )
        print(fs_mj_res.text)
    except:
        pass