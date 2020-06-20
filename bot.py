from pyrogram import Client, Filters, ChatPermissions
from pyrogram import InlineKeyboardMarkup, InlineKeyboardButton
import pyrogram.errors

welcome_message = "Hey, I only works for @viperadnan"
BOT_TOKEN = ""
APP_ID = 
API_HASH = ""
channel_username = "viperpunk"


app = Client("bot", api_id=APP_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_callback_query(Filters.callback_data("onButtonPress"))
def onButtonPress(client, cb):
   user_id = cb.from_user.id
   chat_id = cb.message.chat.id
   try:
     client.get_chat_member(channel_username, user_id)
     client.unban_chat_member(chat_id, user_id)
   except pyrogram.errors.exceptions.bad_request_400.UserNotParticipant:
     client.answer_callback_query(cb.id, text="Join the channel and press the button again.")

@app.on_message(Filters.command(['start', 'help']) & Filters.private)
def start(client, message):
   message.reply_text(welcome_message)

@app.on_message(Filters.text & ~Filters.private, group=1)
def SendMsg(client, message):
  user_id = message.from_user.id
  first_name = message.from_user.first_name
  chat_id = message.chat.id
  try:
    client.get_chat_member(channel_username, user_id)
    return
  except pyrogram.errors.exceptions.bad_request_400.UserNotParticipant:
    message.reply_text(
      "[{}](tg://user?id={}), you are **not subscribed** to my [channel](https://t.me/{}) yet. Please [join](https://t.me/{}) and **press the button below** to unmute yourself.".format(first_name, user_id, channel_username, channel_username),
      disable_web_page_preview=True,
      reply_markup=InlineKeyboardMarkup(
          [[InlineKeyboardButton("UnMute Me", callback_data="onButtonPress")]]
      )
    )
    client.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=False))

app.run()
