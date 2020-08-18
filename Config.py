import os

class Config():
  ENV = bool(os.environ.get('ENV', False))
  if ENV:
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
    DATABASE_URL = os.environ.get("DATABASE_URL", None)
    APP_ID = os.environ.get("APP_ID", 6)
    API_HASH = os.environ.get("API_HASH", None)
    SUDO_USERS = set(int(x) for x in os.environ.get("SUDO_USERS", "939425014").split())
  else:
    BOT_TOKEN = ""
    DATABASE_URL = ""
    APP_ID = ""
    API_HASH = ""
    SUDO = set(int(x) for x in ''.split())


class Messages():
      HELP_MSG = [
        ".",

        "**Force Subscribers**\nForce group members to join a specific channel before sending messages in the group.\n\n**Setup**\n**Step 1.** __Add me in a group(in which you are creator of the group) as admin.__\n**Step 2.** __Send__ `/ForceSubscribe {your channel username}`\n**Step 3.** __Add me to your channel as admin.__\n\n`All set ! I mute users who didn't joined your channel and ask them to join channel and unmute themself.`\n\n**Commands**\n\n/ForceSubscribe { off / no / disable} - To stop force subscriber\n\n/ForceSubscribe {Channel Username} - Set the Channel\n\n/ForceSubscribe - Get current Status",
        
        "**Developed by @viperadnan**\n\nPowered by @viperpunk\nThanks to - @PyroGram @HasibulKobir"
      ]

      START_MSG = "Hey [{}](tg://user?id={})\nI am a multifunctional group manager bot.\nLearn more at /help"