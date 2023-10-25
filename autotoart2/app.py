from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import configparser
import random

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        print(body, signature)
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return 'OK'


# @handler.add(MessageEvent, message=TextMessage)
# def prettyEcho(event):
#     sendString = ""
#     if "抽塔羅" in event.message.text or "塔羅" in event.message.text:
#         random_number, description = divinationBlocks()
#         sendString = "抽到的塔羅牌是：{}\n說明內容是：{}".format(random_number, description)
#     elif "隨機選號碼" in event.message.text:
#         random_numbers = random_select_numbers()
#         sendString = "隨機選取的两个数字是：{}".format(random_numbers)
#     else:
#         sendString = event.message.text
#
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=sendString)
#     )
@handler.add(MessageEvent, message=TextMessage)
def prettyEcho(event):
    sendString = ""
    if "抽塔羅" in event.message.text or "塔羅" in event.message.text:
        random_number, description = divinationBlocks()
        sendString = "抽到的塔羅牌是：{}\n說明內容是：{}".format(random_number, description)
    elif "隨機選號碼" in event.message.text:
        random_numbers, descriptions = random_select_numbers_and_descriptions()
        sendString = "隨機選取的两个数字是：{}\n對應的描述分別是：\n{}".format(random_numbers, '\n'.join(descriptions))
    else:
        sendString = event.message.text

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=sendString)
    )



# 定義一個函式來隨機選取塔羅牌和對應的說明
def divinationBlocks():
    def load_tarot_descriptions(file_path):
        description_dict = {}
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) >= 2:
                    card_number = int(parts[0])
                    description = parts[1]
                    description_dict[card_number] = description
        return description_dict

    # 在代码的开始处调用该函数来加载描述信息
    description_dict = load_tarot_descriptions('tarot_descriptions.txt')
    random_number = random.randint(0,78)
    description = description_dict.get(random_number, "找不到對應的說明內容")
    return random_number, description

# 新增一个函数来随机选取两个不重复的数字
# 新增一个函数来随机选取两个不重复的数字和对应的描述信息
def load_tarot_descriptions(param):
    pass


def random_select_numbers_and_descriptions():
    description_dict = load_tarot_descriptions('tarot_descriptions.txt')
    random_numbers = random.sample(range(79), 2)
    descriptions = [description_dict.get(number, "找不到對應的說明內容") for number in random_numbers]
    return random_numbers, descriptions











if __name__ == "__main__":
    app.run()
