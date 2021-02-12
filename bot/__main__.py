import shutil, psutil
import signal
import pickle

from os import execl, path, remove
from sys import executable
import time

from telegram.ext import CommandHandler, run_async
from bot import dispatcher, updater, botStartTime
from bot.helper.ext_utils import fs_utils
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import *
from bot.helper.ext_utils.bot_utils import get_readable_file_size, get_readable_time
from bot.helper.telegram_helper.filters import CustomFilters
from bot.modules import authorize, list, cancel_mirror, mirror_status, mirror, clone, watch, delete, speedtest, information


@run_async
def stats(update, context):
    currentTime = get_readable_time((time.time() - botStartTime))
    total, used, free = shutil.disk_usage('.')
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
    recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
    cpuUsage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    stats = f'<b>⏰ Bot Uptime : {currentTime} 🤖</b>\n' \
            f'<b>💨 Total Disk Space : {total}</b>\n' \
            f'<b>📈 Used : {used}</b> ' \
            f'<b>📉 Free : {free}</b>\n\n' \
            f'<b>📊 Data Usage 📊</b>\n<b>🔺 Upload : {sent}</b>\n' \
            f'<b>🔻 Download : {recv}</b>\n\n📊 <b>Performance Meter</b> 📊\n\n' \
            f'<b> 🖥️ CPU  : {cpuUsage}%</b>\n ' \
            f'<b>⚙️ RAM : {memory}%</b>\n ' \
            f'<b>🗃️ Disk  : {disk}%</b>'
    sendMessage(stats, context.bot, update)


@run_async
def start(update, context):
    start_string = f'''
This is a bot which can mirror all your links to Google Drive!
Type /{BotCommands.HelpCommand} to get a list of available commands
'''
    sendMessage(start_string, context.bot, update)


@run_async
def restart(update, context):
    restart_message = sendMessage("Restarting, Please wait!", context.bot, update)
    # Save restart message object in order to reply to it after restarting
    fs_utils.clean_all()
    with open('restart.pickle', 'wb') as status:
        pickle.dump(restart_message, status)
    execl(executable, executable, "-m", "bot")


@run_async
def ping(update, context):
    start_time = int(round(time.time() * 1000))
    reply = sendMessage("Starting Ping", context.bot, update)
    end_time = int(round(time.time() * 1000))
    editMessage(f'{end_time - start_time} ms', reply)


@run_async
def log(update, context):
    sendLogFile(context.bot, update)


@run_async
def bot_help(update, context):
    help_string = f'''
/{BotCommands.MirrorCommand} [mega.nz link] [magnet-link] / [torrent-magnet] [direct-link] [download_url] [zippyshare] [mediafire] [github.com link] [osdn.net link] [yadi.sk] : Start Mirroring to Google Drive

/{BotCommands.UnzipMirrorCommand} [mega.nz link] [magnet-link] / [torrent-magnet] [direct-link] [download_url] [zippyshare] [mediafire] [github.com link] [osdn.net link] [yadi.sk] : Start Mirroring. If File is Archive, Extracts it to Google Drive

/{BotCommands.TarMirrorCommand} [mega.nz link] [magnet-link] / [torrent-magnet] [direct-link] [download_url] [zippyshare] [mediafire] [github.com link] [osdn.net link] [yadi.sk] : Start Mirroring & Upload With Archived File (.tar) Extentions

/{BotCommands.WatchCommand} : Mirror Via YouTube-DL. Click /{BotCommands.WatchCommand} For More Help

/{BotCommands.TarWatchCommand} : Mirror Via YouTube-DL and Upload Archive File With (.tar) Extention

/{BotCommands.CancelMirror} : Reply to your mirror download message or use /{BotCommands.CancelMirror} [GID]

/{BotCommands.StatusCommand} : Shows a Status of all the Downloads

/{BotCommands.ListCommand} : Search For Files / Folders on Google Drive. If Found, the bot will reply with a link

/{BotCommands.SpeedCommand} : Check Internet Speed Test

'''
    sendMessage(help_string, context.bot, update)


def main():
    fs_utils.start_cleanup()
    # Check if the bot is restarting
    if path.exists('restart.pickle'):
        with open('restart.pickle', 'rb') as status:
            restart_message = pickle.load(status)
        restart_message.edit_text("Restarted Successfully!")
        remove('restart.pickle')

    start_handler = CommandHandler(BotCommands.StartCommand, start,
                                   filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    ping_handler = CommandHandler(BotCommands.PingCommand, ping,
                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    restart_handler = CommandHandler(BotCommands.RestartCommand, restart,
                                     filters=CustomFilters.owner_filter)
    help_handler = CommandHandler(BotCommands.HelpCommand,
                                  bot_help, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    stats_handler = CommandHandler(BotCommands.StatsCommand,
                                   stats, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    log_handler = CommandHandler(BotCommands.LogCommand, log, filters=CustomFilters.owner_filter)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(ping_handler)
    dispatcher.add_handler(restart_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(stats_handler)
    dispatcher.add_handler(log_handler)
    updater.start_polling()
    LOGGER.info("Bot Started!")
    signal.signal(signal.SIGINT, fs_utils.exit_clean_up)


main()
