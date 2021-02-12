import threading


from telegram import Bot, Update
from bot import dispatcher, AUTHORIZED_CHATS
from telegram.ext import CallbackContext, Filters, run_async, CommandHandler
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from bot.helper.telegram_helper.message_utils import update_all_messages, sendMessage, sendStatusMessage

@run_async
def _fyinfo(bot: Bot, update):
    mssg = update.message.text
    message_args = mssg.split(' ')
    name_args = mssg.split('|')
    try:
        link = message_args[1]
    except IndexError:
        msg = f"TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST "
        sendMessage(msg, bot, update)
        return
    try:
      if "|" in mssg:
        mssg = mssg.split("|")
        qual = mssg[0].split(" ")[2]
        if qual == "":
          raise IndexError
      else:
        #qual = message_args[2]
      #if qual != "audio":
        #qual = f'bestvideo[height<={qual}]+bestaudio/best[height<={qual}]'
    #except IndexError:
      #qual = "bestvideo+bestaudio/best"
    try:
      name = name_args[1]
    except IndexError:
      name = ""
    reply_to = update.message.reply_to_message
    if reply_to is not None:
        tag = reply_to.from_user.username
    else:
        #tag = None
    #pswd = ""
    #listener = MirrorListener(bot, update, pswd, isTar, tag)
    #ydl = YoutubeDLHelper(listener)
    #threading.Thread(target=ydl.add_download,args=(link, f'{DOWNLOAD_DIR}{listener.uid}', qual, name)).start()
    #sendStatusMessage(update, bot)
    #if len(Interval) == 0:
        #Interval.append(setInterval(DOWNLOAD_STATUS_UPDATE_INTERVAL, update_all_messages))


#@run_async
#def fyinfoTar(update, context):
    #_fyinfo(context.bot, update, True)


def fyinfo(update, context):
    _fyinfo(context.bot, update)


INFORMATION_HANDLER = CommandHandler(BotCommands.InformationCommand, fyinfo,
                                filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
#tar_mirror_handler = CommandHandler(BotCommands.TarfyinfoCommand, fyinfoTar,
                                    #filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
									
dispatcher.add_handler(INFORMATION_HANDLER)
#dispatcher.add_handler(tar_mirror_handler)
