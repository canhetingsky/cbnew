#!/usr/bin/python3
# encoding: utf-8
import requests
from requests.models import Response


class Message:
    def __init__(self, sendkey: str) -> None:
        self.sendkey = sendkey

    def send(self, title: str, desp: str = '') -> bool:
        url = 'https://sctapi.ftqq.com/{0}.send'.format(self.sendkey)
        data = {
            'title': title,  # 消息标题，必填。最大长度为 32
            'desp': desp  # 消息内容，选填。支持 Markdown语法 ，最大长度为 32KB ,消息卡片截取前 30 显示
        }
        response = requests.post(url, data=data)
        code = response.status_code
        if code == 200:
            return True
        else:
            print('消息发送失败(代码：{0})'.format(code))
            return False


if __name__ == '__main__':
    pass
