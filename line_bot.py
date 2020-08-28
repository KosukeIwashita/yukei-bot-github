from flask import Flask, request, abort

from linebot import (
   LineBotApi, WebhookHandler
)
from linebot.exceptions import (
   InvalidSignatureError
)
from linebot.models import (
   MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('l93wr01BmymtABAEVZxmWQ/QEl/ipfVjemoA4s6ClYQZ1SpTJIBQaddiMMM4bixbs94c6DSOOv+2CaOpF6tjDKqK/JtB7JhphBrXLK8z43Xjl7IMdmQGAVTnxHz9k+Utd9kgUw5eli6+F1LJUQSqaAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2bd122c701510001c9bd7d68c536a1c5')


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
       print("Invalid signature. Please check your channel access token/channel secret.")
       abort(400)

   return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
   line_bot_api.reply_message(
       event.reply_token,
       TextSendMessage(text=event.message.text))


if __name__ == "__main__":
   app.run(host='127.0.0.1', port=8080, debug=True)
