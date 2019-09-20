# youtube-telegram-bot-python
Creating a bot that given a youtube link downloads it and uploads to telegram channel


### Setup
pip install -r requirements.txt


### Functions

/ytsearch: works as a search like youtube search. Given the keywords finds the first 10 videos in youtube and gives the links. 

Copy and paste the link and the bot will download the video to a given working directory change the name and upload it to a channel you listed (bot should be an admin of that channel). After the upload, it automatically deletes the video from your directory.


### Variables to modify

1) "<telegram_bot_token>"
2) "<path_of_your_directory>"
3) "<file_name>"
4) "<sample_channel>"


### NOTES:
So far bot can only upload videos up to 50MB. The bot automatically checks it and responds with "the file was too large (-_-) (max 50MB)" message.

Below you can find a link about how to open your bot in telegram and get the token.

https://core.telegram.org/bots
