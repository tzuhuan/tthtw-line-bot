from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerMessage, StickerSendMessage,
    ImageSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction
)

import configparser
from modules import ptt, stock, randomcat, randomwife

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
            '揍/punch\n'
            'ptt [版名] [關鍵字]\n'
            'stock [代號]')
    
def SendPunchSticker(event):
    sticker_message = StickerMessage(package_id='2', sticker_id=147)
    line_bot_api.reply_message(event.reply_token, sticker_message)   

def quick_menu(event):
    bottons_template = TemplateSendMessage(
        alt_text='TTHTW template',
        template=ButtonsTemplate(
            title='TTHTW Quick Menu',
            text='請選擇',
            actions=[
                MessageTemplateAction(
                    label='貓貓圖',
                    text='貓貓圖'),
                MessageTemplateAction(
                    label='2018 世足賽',
                    text='fifa')
                   ]
            )
        )
    
    line_bot_api.reply_message(event.reply_token, bottons_template)
    
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    reply_message = ''
    received_msg = event.message.text.lower()    
    commands = received_msg.split()
    
    if received_msg.find('我老婆') != -1:
        wife = randomwife.RandomWife()
        url = wife.query()
        line_bot_api.reply_message(event.reply_token, ImageSendMessage(url, url))
        return
    elif commands[0] == 'tthtw':
        if len(commands) == 1:
            quick_menu(event)
            return
        else:
            reply_message = ptt.query(received_msg)
    elif commands[0] == 'fifa':
        reply_message = ptt.fifa()
    elif commands[0] == 'punch' or commands[0] == '揍':
        SendPunchSticker(event)
        return
    elif commands[0] == 'help':
        reply_message = help()
    elif commands[0] == 'stock':
        stock_obj = stock.Stock()
        if len(commands) > 1:
            reply_message = stock_obj.query(commands[1])
        else:
            return
    elif commands[0] == 'tth':
        image_message = ImageSendMessage('https://pic.pimg.tw/jackaly9527/4a608dbd1c3fa.jpg', 'https://pic.pimg.tw/jackaly9527/4a608dbd1c3fa.jpg')
        line_bot_api.reply_message(event.reply_token, image_message)
        return
    elif commands[0] == '貓貓圖':
        cat = randomcat.RandomCat()
        url = cat.query()
        image_message = ImageSendMessage(url, url)
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
