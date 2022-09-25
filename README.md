# python4twitch

Prerequisites: Python installed, knowledge to edit and run Python scripts.

1. Get Twitch chat token here: https://twitchapps.com/tmi/ 
    In T2Tbot.py edit self.nickname and self.TwitchToken.

2. Create A Telegram Bot Using Telegram’s BotFather
    Open Telegram app and search for BotFather.
    Type /newbot to create a new bot. After completing the bot setup you'll get the Telegram bot’s token.

3. In Telegram bot chat send a random message (e.g. test) to your bot. 
    Edit Telegram bot's token in get_chat_id.py and run the script.
    In the result look for 'chat': {'id': 
    The number behind it is the Chat Id.

4. Create telegram_id.txt in Notepad. Type 0 in it and save in the same folder as the script.

5. Put channels and keywords in self.channels and self.keywords respectively.
