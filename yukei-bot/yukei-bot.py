from flask import Flask,request,abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage
import os
import requests
import pprint
import pya3rt

app=Flask(__name__)
#環境変数の取得
YOUR_CHANNEL_ACCESS_TOKEN="line_channel_token"
YOUR_CHANNEL_SECRET="line_channel_secret"
line_bot_api=LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler=WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback",methods=["POST"])
def callback():
    signature=request.headers["X-Line-Signature"]

    body=request.get_data(as_text=True)
    app.logger.info("Request body"+body)

    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    #入力された文字列を格納
    push_text = event.message.text

    #A3RTのTalkAPIにより応答
    reply_text = talkapi_response(push_text)

    #リプライ部分の記述
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_text))

#A3RTのTalkAPIにより応答
def talkapi_response(text):
    apikey = "tk_ap"
    client = pya3rt.TalkClient(apikey)
    response = client.talk(text)
    return ((response['results'])[0])['reply']

if __name__=="__main__":
    port=int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0",port=port)
