from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.exceptions import *
from linebot.models import *
#from linebot.exceptions import (
#    InvalidSignatureError
#)
#from linebot.models import (
#    MessageEvent, TextMessage, TextSendMessage, StickerMessage, StickerSendMessage,
#    ImageSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction
#)

import configparser
from modules import ptt, stock, randomcat, randomwife, randomuser, randomdaughter, randombird

#
from modules import ptt_widget, random_dog
import random
import time
#
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

def chi_ptt_widget(event):
    time_beginTimer = time.time()
    ptt_beauty = ptt_widget.BroadCrawler('Beauty')
        
    luckyArticle = None
    lst_imgUrls = None
    while(luckyArticle is None):
        int_luckyIndex = ptt_beauty.get_last_page_index() - random.randint(0, ptt_widget.INT_RANDOM_LIMIT)
        if not int_luckyIndex > 0:
            continue
         
        lst_articles = list()
        lst_articles.extend(ptt_beauty.get_article_links(int_luckyIndex))
        if not len(lst_articles) > 0:
            continue
            
        int_luckyPage = random.randint(0, len(lst_articles) - 1)
        for article in lst_articles[int_luckyPage:]:
            print ('debug: select %s' % article)
            lst_imgUrls = article.get_thumb_list()
            if not lst_imgUrls is None:
                print ('debug: %s' % lst_imgUrls)
                luckyArticle = article
                break
    print ('debug: chose %s' % luckyArticle.dict_info['str_title'])
    print ('debug: url >>> %s' % luckyArticle.dict_info['str_url'])
        
    lst_carouselColumns = list()
    lst_label = luckyArticle.get_split_label()
    for index, imgUrl in enumerate(lst_imgUrls):
        print ('debug: +%s' % imgUrl)
        lst_carouselColumns.append(
            ImageCarouselColumn(
                image_url = imgUrl,
                #action=MessageAction(
                #        label = lst_label[index%len(lst_label)],
                #        text='我覺得圖[%d]很可以！\n\n%s\n%s' % (index+1, luckyArticle.dict_info['str_title'], luckyArticle.dict_info['str_url'])
                #)
                action=URITemplateAction(
                        label = lst_label[index%len(lst_label)],
                        uri = luckyArticle.dict_info['str_url']
                )
            )
        )
        if len(lst_carouselColumns) >= 5:
            break
        
    imageCarousel = TemplateSendMessage(
        alt_text = '%s\n%s' % (luckyArticle.dict_info['str_title'], luckyArticle.dict_info['str_url']),
        template = ImageCarouselTemplate(columns = lst_carouselColumns)
    )
        
    print('debug: Image Carousel: %s' % imageCarousel)
    print('debug: Cost: %.2f sec' % (time.time() - time_beginTimer))
       
    reply_msg = imageCarousel
    print('debug: error check: %s' % reply_msg)
    line_bot_api.reply_message(event.reply_token, reply_msg)
    
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
    elif received_msg.find('我女兒') != -1:
        daughter = randomdaughter.RandomDaughter()
        url = daughter.query()
        line_bot_api.reply_message(event.reply_token, ImageSendMessage(url, url))
        return
    elif commands[0] == 'ptt':
        reply_message = ptt.query(received_msg)
    elif commands[0] == 'pttaa':
        title, url = ptt.query(received_msg)
        reply = [TextSendMessage(text=title)]
        if url == '???':
            reply = StickerMessage(package_id='1', sticker_id=17)
        else:
            reply.append(ImageSendMessage(url, url))
        line_bot_api.reply_message(event.reply_token, reply)
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
    elif commands[0] == '狗狗圖':
        dog = random_dog.RandomDog()
        url = dog.query()
        image_message = ImageSendMessage(url, url)
        line_bot_api.reply_message(event.reply_token, image_message)
        return
    elif commands[0] == '鳥鳥圖':
        bird = randombird.RandomBird()
        url = bird.query()
        image_message = ImageSendMessage(url, url)
        line_bot_api.reply_message(event.reply_token, image_message)
        return   
    #elif commands[0] == 'randomuser':
    #    user = randomuser.RandomUser()
    #    url = user.query()
    #    line_bot_api.reply_message(event.reply_token, ImageSendMessage(url, url))
    elif commands[0] == '表特霸':
        chi_ptt_widget(event)
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
    # test
    app.run()
