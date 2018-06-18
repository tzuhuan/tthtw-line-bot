from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerMessage, StickerSendMessage,
)

import ptt, configparser

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

def SendPunchSticker(event):
    sticker_message = StickerMessage(package_id='2', sticker_id=147)
    line_bot_api.reply_message(event.reply_token, sticker_message)   

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    reply_message = ''

    if event.message.text.lower() == 'ptto2':
        urls = ptt.o2()
        for url in urls:
            reply_message += url
    elif event.message.text.lower() == 'fifa':
        reply_message = ptt.fifa()
    elif event.message.text.lower() == 'punch' or event.message.text == '揍':
        SendPunchSticker(event)
        return
    elif event.message.text.lower() == 'help':
        reply_message = 'Supported commands:\nfifa\n揍\npunch'
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
