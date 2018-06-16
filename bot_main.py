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

app = Flask(__name__)

line_bot_api = LineBotApi('BuhgBcv9EZuqq4enk25URlqliZiOVvU8DSddmNzEz7UGJWLITA9RHMZAaX/B/2vNoQ1JK+C4ABG0JvZ76mBZYw2wVjRzzhdBytaD6lqGd3JcaY2eO19M8ti6BacaitPfX54231wsRAjKHYoR27934QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('21966c724075b8636306fb9d7f47201a')


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='>> ' + event.message.text))

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    reply_msg = 'id = ' + event.message.id + ', package_id = ' + event.message.package_id + ', sticker_id = ' + event.message.sticker_id
    line_bot_api.reply_message(
	    event.reply_token,
		TextSendMessage(text=reply_msg))
		
	sticker_message = StickerMessage(package_id='1', sticker_id='13')
	line_bot_api.reply_message(event.reply_token, sticker_message)
		
if __name__ == "__main__":
    app.run()