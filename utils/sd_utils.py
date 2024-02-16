import requests
import base64
from PIL import Image
from io import BytesIO


class SD:
    def __init__(self, baseurl, username, password):
        self.baseurl = baseurl
        self.username = username
        self.password = password

    # 文生图
    def txt2img(self, params):
        response = requests.request(
            method="POST",
            url="{}/sdapi/v1/txt2img".format(self.baseurl),
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json'
            },
            auth=(self.username, self.password),
            json=params
        )
        return response.json()

    # 图生图
    def img2img(self, params):
        response = requests.request(
            method="POST",
            url="{}/sdapi/v1/img2img".format(self.baseurl),
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json'
            },
            auth=(self.username, self.password),
            json=params
        )
        return response.json()

    # 获取 png_info
    def png_info(self, image_data):
        response = requests.request(
            method="POST",
            url="{}/sdapi/v1/png-info".format(self.baseurl),
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json'
            },
            auth=(self.username, self.password),
            json={
                "image": image_data
            }
        )
        return response.json()

    # controlnet 模型列表
    def model_list(self):
        response = requests.request(
            method="GET",
            url="{}/controlnet/model_list".format(self.baseurl),
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json'
            },
            auth=(self.username, self.password)
        )
        return response.json()

    # 保存图片到指定文件
    def image_data_to_file(self, encoded_image_str, image_path):
        # 将字符串进行 base64 解码
        image_data = base64.b64decode(encoded_image_str)
        # 将解码后的字节流转换为图片对象
        image = Image.open(BytesIO(image_data))
        # 保存图片对象到文件
        image.save(image_path)

    # 将文件转换成图片数据
    def file_to_image_data(self, image_path):
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
        # 将字节流进行 base64 编码
        encoded_image_data = base64.b64encode(image_data)
        # 转换为字符串
        return encoded_image_data.decode()
