from pyrogram import Filters, ChatPermissions
from pyrogram import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client as app
import pyrogram.errors
import sql_helpers.forceSubscribe_sql as sql



@app.on_callback_query(Filters.callback_data("onButtonPress"))
def onButtonPress(client, cb):
   user_id = cb.from_user.id
   chat_id = cb.message.chat.id
   cws = sql.fs_settings(chat_id)
   if cws:
     CHANNEL_USERNAME = cws.channel
   try:
     client.get_chat_member(CHANNEL_USERNAME, user_id)
     client.unban_chat_member(chat_id, user_id)
   except pyrogram.errors.exceptions.bad_request_400.UserNotParticipant:
     client.answer_callback_query(cb.id, text="Join the channel and press the button again.")


@app.on_message(Filters.text & ~Filters.private, group=1)
def SendMsg(client, message):
  cws = sql.fs_settings(message.chat.id)
  if not cws:
    return
  user_id = message.from_user.id
  first_name = message.from_user.first_name
  CHANNEL_USERNAME = cws.channel
  try:
    client.get_chat_member(CHANNEL_USERNAME, user_id)
    return
  except pyrogram.errors.exceptions.bad_request_400.UserNotParticipant:
    if client.get_chat_member(message.chat.id, user_id).status in ("administrator", "creator"):
      return
    message.reply_text(
      "[{}](tg://user?id={}), you are **not subscribed** to my [channel](https://t.me/{}) yet. Please [join](https://t.me/{}) and **press the button below** to unmute yourself.".format(first_name, user_id, CHANNEL_USERNAME, CHANNEL_USERNAME),
      disable_web_page_preview=True,
      reply_markup=InlineKeyboardMarkup(
          [[InlineKeyboardButton("UnMute Me", callback_data="onButtonPress")]]
      )
    )
    client.restrict_chat_member(message.chat.id, user_id, ChatPermissions(can_send_messages=False))
  except pyrogram.errors.exceptions.bad_request_400.ChatAdminRequired:
    client.send_message(message.chat.id, text=f"I am not an admin in @{CHANNEL_USERNAME}")
  except ValueError:
    client.send_message(message.chat.id, text=f"I am not an admin in @{CHANNEL_USERNAME}")


@app.on_message(Filters.command(["forcesubscribe"]) & ~Filters.private)
def config(client, message):
  user = client.get_chat_member(message.chat.id, message.from_user.id)
  if user.status is "creator":
    chat_id = message.chat.id
    try:
      input_str = message.command[1]
      input_str = input_str.replace("@", "")
    except IndexError:
      if sql.fs_settings(chat_id):
        message.reply_text(f"Force Subscribe is **enabled** in this chat.\nChannel - @{sql.fs_settings(chat_id).channel}")
        return
      else:
        message.reply_text("Force Subscribe is **disabled** in this chat.")
        return
    if input_str.lower() in ("off", "no", "disable"):
      sql.disapprove(chat_id)
      message.reply_text("Force Subscribe is **Disabled**")
    elif input_str:
      try:
        client.get_chat_member(input_str, "me")
        sql.add_channel(chat_id, input_str)
        message.reply_text(f"Force Subscribe is **enabled** for this chat\nChannel - @{input_str}")
      except pyrogram.errors.exceptions.bad_request_400.UserNotParticipant:
        message.reply_text(f"I am not an admin in @{input_str}\nAdd me on your channel as admin and send the command again.")
      except pyrogram.errors.exceptions.bad_request_400.UsernameNotOccupied:
        message.reply_text(f"Invalid Channel Username")
      except ValueError:
        message.reply_text(f"@{input_str} didn't belongs to a channel.")
    else:
      message.reply_text("Something went wrong")
  else:
    message.reply_text("You have to be the **Group Creator** to do that.")