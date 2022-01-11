import time
import logging
from Config import Config
from pyrogram import Client, filters
from sql_helpers import forceSubscribe_sql as sql
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid

logging.basicConfig(level=logging.INFO)

static_data_filter = filters.create(lambda _, __, query: query.data == "onUnMuteRequest")
@Client.on_callback_query(static_data_filter)
def _onUnMuteRequest(client, cb):
  user_id = cb.from_user.id
  chat_id = cb.message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    channel_s = chat_db.channel.split(".")
    chat_member = client.get_chat_member(chat_id, user_id)
    if chat_member.restricted_by:
      if chat_member.restricted_by.id == (client.get_me()).id:
        n_subscription_s = []
        for channel in channel_s:
          try:
            client.get_chat_member(channel, user_id)
          except UserNotParticipant:
            n_subscription_s.append(channel)
          if len(n_subscription_s) > 0:
            client.answer_callback_query(
              cb.id,
              text="❗ Join the mentioned 'channel(s)' and press the 'UnMute Me' button again.",
              show_alert=True
            )
          else:
            client.unban_chat_member(chat_id, user_id)
            if cb.message.reply_to_message.from_user.id == user_id:
              cb.message.delete()
      else:
        client.answer_callback_query(cb.id, text="❗ You are muted by admins for other reasons.", show_alert=True)
    else:
      if not client.get_chat_member(chat_id, (client.get_me()).id).status == 'administrator':
        client.send_message(chat_id, f"❗ **{cb.from_user.mention} is trying to UnMute himself but i can't unmute him because i am not an admin in this chat add me as admin again.**\n__#Leaving this chat...__")
        client.leave_chat(chat_id)
      else:
        client.answer_callback_query(cb.id, text="❗ Warning: Don't click the button if you can speak freely.", show_alert=True)



@Client.on_message(filters.text & ~filters.private & ~filters.edited, group=1)
def _check_member(client, message):
  chat_id = message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    user_id = message.from_user.id
    if not client.get_chat_member(chat_id, user_id).status in ("administrator", "creator") and not user_id in Config.SUDO_USERS:
      channels = chat_db.channel.split(".")
      n_subscription_s = []
      for channel in channels:
        try:
          client.get_chat_member(channel, user_id)
        except UserNotParticipant:
          n_subscription_s.append(channel)
        except ChatAdminRequired:
          client.send_message(chat_id, text=f"❗ **I am not an admin in @{channel}**\n__Make me admin in the channel and add me again.\n#Leaving this chat...__")
          sql.disapprove(chat_id)
          client.leave_chat(chat_id)
          return
      if len(n_subscription_s) > 0:
        mmo = "@" + " @".join(n_subscription_s)
        try:
          sent_message = message.reply_text(
              "{}, you are **not subscribed** to my channels: {mmo} yet. Please [join](https://t.me/{}) and **press the button below** to unmute yourself.".format(message.from_user.mention, channel, channel),
              disable_web_page_preview=True,
              reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton("UnMute Me", callback_data="onUnMuteRequest")]]
              )
          )
          client.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=False))
        except ChatAdminRequired:
          sent_message.edit("❗ **I am not an admin here.**\n__Make me admin with ban user permission and add me again.\n#Leaving this chat...__")
          client.leave_chat(chat_id)


@Client.on_message(filters.command(["forcesubscribe", "fsub"]) & ~filters.private)
def config(client, message):
  user = client.get_chat_member(message.chat.id, message.from_user.id)
  if user.status == "creator" or user.user.id in Config.SUDO_USERS:
    chat_id = message.chat.id
    if len(message.command) > 1:
      input_str = message.command[1]
      input_str = input_str.replace("@", "")
      if input_str.lower() in ("off", "no", "disable"):
        sql.disapprove(chat_id)
        message.reply_text("❌ **Force Subscribe is Disabled Successfully.**")
      elif input_str.lower() in ('clear'):
        sent_message = message.reply_text('**Unmuting all members who are muted by me...**')
        try:
          for chat_member in client.get_chat_members(message.chat.id, filter="restricted"):
            if chat_member.restricted_by.id == (client.get_me()).id:
                client.unban_chat_member(chat_id, chat_member.user.id)
                time.sleep(1)
          sent_message.edit('✅ **UnMuted all members who are muted by me.**')
        except ChatAdminRequired:
          sent_message.edit('❗ **I am not an admin in this chat.**\n__I can\'t unmute members because i am not an admin in this chat make me admin with ban user permission.__')
      else:
        swo, wso = get_valid_channels(message)
        if not swo:
          message.reply_text(wso, disable_web_page_preview=True)
          return
        input_str = ".".join(wso)
        mmo = "@" + " @".join(wso)
        sql.add_channel(chat_id, input_str)
        message.reply_text(
          f"✅ **Force Subscribe is Enabled**\n__Force Subscribe is enabled, all the group members have to subscribe these {mmo} channels in order to send messages in this group.__",
          disable_web_page_preview=True
        )
    else:
      if sql.fs_settings(chat_id):
        message.reply_text(f"✅ **Force Subscribe is enabled in this chat.**\n__For this [Channel](https://t.me/{sql.fs_settings(chat_id).channel})__", disable_web_page_preview=True)
      else:
        message.reply_text("❌ **Force Subscribe is disabled in this chat.**")
  else:
      message.reply_text("❗ **Group Creator Required**\n__You have to be the group creator to do that.__")


def get_valid_channels(message: Message):
  channel_pors = message.command[1:]
  channel_srop = []
  for input_str in channel_pors:
    input_str = input_str.replace("@", "")
    try:
      client.get_chat_member(input_str, "me")
      channel_srop.append(input_str)
    except UserNotParticipant:
      return False, f"❗ **Not an Admin in the Channel**\n__I am not an admin in the [channel](https://t.me/{input_str}). Add me as a admin in order to enable ForceSubscribe.__"
    except (UsernameNotOccupied, PeerIdInvalid):
      message.reply_text()
      return False, f"❗ **Invalid Channel Username.**"
    except Exception as err:
      return False, f"❗ **ERROR:** ```{err}```"
  return True, channel_srop
