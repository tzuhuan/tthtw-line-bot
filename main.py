from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerMessage, StickerSendMessage, ImageSendMessage,
)

import ptt, configparser
import stock

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config['tthtw-line-bot']['Channel_Access_Token'])
handler = WebhookHandler(config['tthtw-line-bot']['Channel_Secret'])


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def help():
    return ('fifa\n'
            '揍\n'
            'punch\n'
            'stock [stock_number]. Default is tsmc')
    
def SendPunchSticker(event):
    sticker_message = StickerMessage(package_id='2', sticker_id=147)
    line_bot_api.reply_message(event.reply_token, sticker_message)   

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    reply_message = ''

    commands = event.message.text.lower().split()
    if commands[0] == 'ptto2':
        urls = ptt.o2()
        for url in urls:
            reply_message += url
    elif commands[0] == 'fifa':
        reply_message = ptt.fifa()
    elif commands[0] == 'punch' or commands[0] == '揍':
        SendPunchSticker(event)
        return
    elif commands[0] == 'help':
        reply_message = help()
    elif commands[0] == 'ptthelp':
        reply_message = ptt.help()
    elif commands[0] == 'pttstock':
        if len(commands) > 1:
            reply_message = ptt.stock(commands[1])
        else:
            reply_message = ptt.stock()
    elif commands[0] == 'pttbeauty':
        if len(commands) > 1:
            reply_message = ptt.beauty(commands[1])
        else:
            reply_message = ptt.beauty()
    elif commands[0] == 'stock':
        stock_obj = stock.Stock()
        if len(commands) > 1:
            reply_message = stock_obj.query(commands[1])
        else:
            reply_message = stock_obj.query()
    elif commands[0] == 'tth':
        image_message = ImageSendMessage('https://pic.pimg.tw/jackaly9527/4a608dbd1c3fa.jpg', 'https://pic.pimg.tw/jackaly9527/4a608dbd1c3fa.jpg')
        line_bot_api.reply_message(event.reply_token, image_message)
        return
    else:
        return

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message))

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    #sticker_message = StickerMessage(package_id='1', sticker_id=13)
    #line_bot_api.reply_message(event.reply_token, sticker_message)
	pass
		
if __name__ == "__main__":
    app.run()
