# -*- coding: utf-8 -*-
import asyncio
import os
import pymysql

import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage, Message
from botpy.types.message import MarkdownPayload, KeyboardPayload

taovis_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_group_at_message_create(self, message: GroupMessage):
        if message.content.strip().strip("/") == '今天吃什么':
            # 建立数据库连接
            connection = pymysql.connect(
                host='106.15.0.69',
                port=3306,
                user='taovis',
                passwd='taovis_0424',
                db='errorwft',
                charset='utf8'
            )

            # 创建游标对象
            cursor = connection.cursor()

            cursor.execute(
                "SELECT country,area,name FROM taovis_foods  AS t1  JOIN (SELECT ROUND(RAND() * ((SELECT MAX(id) FROM taovis_foods)-(SELECT MIN(id) FROM taovis_foods))+(SELECT MIN(id) FROM taovis_foods)) AS id) AS t2 WHERE t1.id >= t2.id AND type='菜品' ORDER BY t1.id LIMIT 1")

            result = cursor.fetchone()

            _log.info(f"what_to_eat select result ::: {result}")

            connection.close()

            if result[0] == "中国":
                post_content = f"不如来一份{result[1]}的{result[2]}吧！"
            else:
                post_content = f"不如来一份{result[0]}{result[1]}的{result[2]}吧！"

            await message._api.post_group_message(
                group_openid = message.group_openid,
                msg_type = 0,
                msg_id = message.id,
                content = post_content)
        else:
            await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content=f"还没写好，可以期待，不用等待~")

if __name__ == "__main__":
    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=taovis_config["appid"], secret=taovis_config["secret"])