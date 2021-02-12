from telegram import Bot, Update
from bot.helper.telegram_helper.filters import CustomFilters
from bot import dispatcher, AUTHORIZED_CHATS
from bot.helper.telegram_helper.bot_commands import BotCommands
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackContext, Filters, run_async, CommandHandler
from bot.helper.telegram_helper.message_utils import update_all_messages, sendMessage, sendStatusMessage

def fyi(bot: Bot, update):
    mssg = update.message.text
    message_args = mssg.split(' ')
    name_args = mssg.split('|')
    try:
        link = message_args[1]
    except IndexError:
        msg = f"/{BotCommands.WatchCommand} [yt_dl supported link] [Quality] |[Custom Name] to Mirror with youtube-dL.\n\n"
        msg += "<b>Note :- Quality and Custom Name are Optional</b>\n\nExample of Quality :  audio, 144, 240, 360, 480, 720, 1080, 2160."
        msg += "\n\nIf you want to use custom filename, enter it after |"
        msg += f"\n\nExample :\n<code>/{BotCommands.WatchCommand} https://youtu.be/9jZ01i92JI8 720 |Avengers - EndGame (2019)</code>\n\n"
        msg += "This file will be downloaded in 720p quality and it's name will be <b>Avengers - EndGame (2019)</b>"
        sendMessage(msg, bot, update)


fyinfo_handler = CommandHandler(BotCommands.InformationCommand, fyi,
                                filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
dispatcher.add_handler(fyinfo_handler)
