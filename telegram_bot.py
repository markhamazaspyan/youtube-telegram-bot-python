from __future__ import unicode_literals
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from time import sleep
import glob
import os
import requests
from bs4 import BeautifulSoup
import youtube_dl
import re


TOKEN = "<telegram_bot_token>"
bot = telegram.Bot(TOKEN)

# Answering to the /start command
def start(bot, update):
    update.message.reply_text("please type /ytsearch and input a search items")

# Validating the youtube URL
def youtube_url_validation(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return True
    else:
        return False

# downloading the video
def download_video(bot, update):
    if (youtube_url_validation(update.message.text)) == True or ("m.youtube" in update.message.text):
        link=update.message.text
        update.message.reply_text("downloading...")

        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        list_of_files = glob.glob('<path_of_your_directory>*')
        latest_file = max(list_of_files, key=os.path.getctime)
        while True:
            if os.path.isfile(latest_file)==False:
                sleep(1)
                print("sleep")
            else:
                break
        os.rename(latest_file,"<file_name>."+latest_file.split(".")[-1])
        final_file = os.path.abspath("<file_name>.mp4")
        print(final_file)
        update.message.reply_text("download completed, uploading...")

        if os.path.getsize(final_file)/1000000<50:
            bot.send_document(chat_id="<@sample_channel>", document=open(final_file, 'rb'),timeout=100)
            update.message.reply_text("find the file in '<@sample_channel>'")
            os.remove(final_file)
        else:
            update.message.reply_text("the file was too large (-_-) (max 50MB)")
            os.remove(final_file)
    else:
        update.message.reply_text("stop there - please insert a valid youtube link")


# Replying with the first top 10 videos accourding to the /ytsearch keyword
def start_callback(bot, update, args):
    if len(args)==1:
        search="https://www.youtube.com/results?search_query="+args[0]
    else:
        search="https://www.youtube.com/results?search_query="+("+".join(args))
        print
    response = requests.get(search)
    page = response.text
    soup = BeautifulSoup(page,"lxml")
    links=[]
    for i in soup.find_all("a",{"aria-hidden":"true"}):
        links.append("https://www.youtube.com"+i.attrs['href'])

    for i in links[:10]:
        update.message.reply_text(i)
        sleep(1)
    update.message.reply_text("top 10 youtube videos for the "+" ".join(args))



def main():
  # Create Updater object and attach dispatcher to it
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    print("Bot started")

# Add command handler to dispatcher

    start_handler = CommandHandler('ytsearch',start_callback, pass_args=True)
    dispatcher.add_handler(start_handler)

    start_handler = CommandHandler('start',start)
    dispatcher.add_handler(start_handler)

    start_handler = MessageHandler(Filters.text, download_video)
    dispatcher.add_handler(start_handler)


# Start the bot
    updater.start_polling()

# Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
